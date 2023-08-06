from snowflake.connector.pandas_tools import write_pandas
from typing import List, Optional, Any
import snowflake.connector
from tqdm import tqdm
import pandas as pd
import sqlparse
import time
import os
import re
from ..sql_utils import convert_to_snowflake_syntax, correct_sql_system_variables_syntax
from ..pandas_manager import check_quality_table_names
from .redshift_operator import RedshiftOperator
from .s3_operator import S3Operator


def send_to_snowflake(database: str,
                      schema: str,
                      table: str,
                      df: pd.DataFrame,
                      send_to_s3: bool = False,
                      **kwargs: Any):
    """
    Use this function to send a DataFrame to Snowflake.
    :param database: The database name.
    :param schema: The schema name.
    :param table: The table name.
    :param df: The Dataframe.
    :param send_to_s3: Boolan value to indicate if the function should send the object as well to S3.
    :param kwargs: Extra arguments as 'bucket' with the bucket name.
    :return: None
    """
    # Check if the column names agree with the SQL standards. It must not have accented letters or any special
    # character.
    check_quality_table_names(table_name=table, df=df)

    if send_to_s3:
        so = S3Operator()
        if database.lower() == 'oip':
            so.bucket = kwargs.get("bucket", os.environ.get("S3_BUCKET_DATAMART"))
            raise ValueError("❌ Environment variable missing: S3_BUCKET_DATAMART")
        else:
            so.bucket = kwargs.get("bucket", os.environ.get("S3_BUCKET_DEV"))
            if so.bucket is None:
                raise ValueError("❌ Environment variable missing: S3_BUCKET_DEV")

        so.send_to_s3_obj(df=df, s3_file_path=os.path.join(schema, f"{table}.csv"), sep="|")

    sf = SnowflakeOperator(snowflake_database=database)
    sf.schema = schema
    sf.send_table(df=df, table_name=table)
    sf.conn.close()


def read_from_snowflake(database: str, schema: str, table: str) -> pd.DataFrame:
    """
    Use this function to read data from Snowflake.
    :param database: The database name.
    :param schema: The schema name.
    :param table: The table name.
    :return: Table from Snowflake in pd.Dataframe format.
    """
    sf = SnowflakeOperator(snowflake_database=database)
    sf.schema = schema
    df = sf.get_table(table_name=table)
    sf.conn.close()

    return df


def migrate_data_from_redshift(rs_db: str, sf_db: str,
                               schemas_list: Optional[List] = None,
                               avoid_schemas_list: Optional[List[str]] = None,
                               tables_list: Optional[List] = None,
                               avoid_tables_list: Optional[List[str]] = None,
                               logging: bool = True,
                               verbose: bool = True,
                               schema_migration_dict: Optional[dict] = None) -> List:
    """
    Launch a Data Migration process sending tables from redshift into snowflake.
    :param rs_db: Redshift database name.
    :param sf_db: Snowflake database name.
    :param schemas_list: List of schemas to be migrated.
    :param avoid_schemas_list: List of schemas to be avoided.
    :param tables_list: List of tables to be migrated.
    :param avoid_tables_list: List of tables to be avoided.
    :param logging: Boolean to create or not a query_log_errors.txt listing all the problematic queries.
    :param verbose: Boolean to set a exhaustive printing or not.
    :param schema_migration_dict: If the migration happens to be between schemas with different names,
                                                  we can set this config as a dictionary.
                                                  - For example:
                                                        If we want to migrate the metadata from schema1 in Redshift
                                                        into schema2 in Snowflake, we can set this relation as:
                                                        >>> schema_migration_dict = {schema1: schema2}.
    :return: Two values: 1st a string with the amount of time it took to process everything. 2nd a list with the schema,
    table name and error encountered, if any, when migrating.
    """
    ro = RedshiftOperator(database=rs_db)
    ddl_df = ro.get_DDL(schema_names=schemas_list,
                        avoid_schema_names=avoid_schemas_list,
                        table_names=tables_list,
                        avoid_table_names=avoid_tables_list,
                        verbose=verbose)
    ddl_df.fillna("", inplace=True)

    if schema_migration_dict:
        ddl_df.replace(schema_migration_dict, regex=True, inplace=True)
    if logging:
        if os.path.exists("query_log_errors.txt"):
            os.remove("query_log_errors.txt")

    print("🦆 Migrating Redshift into Snowflake:")
    sf = SnowflakeOperator(snowflake_database=sf_db)
    string_check = re.compile("[\s@\-!#$%^&*+()<>?/\|}{~:]")  # Regex to find special characters.
    all_times_list, error_tables = [], []
    with tqdm(total=ddl_df.__len__(), ncols=150, dynamic_ncols=True) as pb:
        for index, row in ddl_df.iterrows():
            try:
                redshift_schema = row['schema_name']
                table_name = row['table_name']

                # Progression bar description.
                pb.set_description(f"Processing... --> {redshift_schema} | {table_name} ")

                # Checking for table names with non-standard names. In that case, quotes must be added.
                if not table_name.isascii() or (string_check.search(table_name) is not None):
                    table_name = f'"{table_name}"'

                # Retrieving table from redshift as a Pandas Dataframe.
                rs_start = time.time()
                ro._schema = redshift_schema
                ro._table = table_name
                df_from_redshift = ro.read_from_redshift()
                rs_time = time.time() - rs_start

                # It should send to snowflake only if the table isn't empty.
                if df_from_redshift.__len__() != 0:

                    # If any of the column names are non-standard as well quotes must be added. Also, in  Snowflake,
                    # the names 'values' and 'group' must have quotes as well since they are system variables.
                    for col_name in df_from_redshift.columns:
                        if (not col_name.isascii()
                                or (string_check.search(col_name) is not None)
                                or (col_name == "values") or (col_name == "group")):
                            df_from_redshift.rename(columns={col_name: f'"{col_name}"'}, inplace=True)

                    # Retrieving table from redshift as a Pandas Dataframe.
                    sf_start = time.time()
                    sf.schema = redshift_schema
                    sf.send_table(df=df_from_redshift, table_name=table_name)
                    sf_time = time.time() - sf_start

                    all_times_list.append(rs_time + sf_time)
            except Exception as e:
                error_tables.append([redshift_schema, table_name, str(e)])
            finally:
                time.sleep(0.5)
                pb.update(1)

    print("✂️ Checking for tables to drop in case they are no more in Redshift.")
    sf.drop_old_tables(ddl_df=ddl_df)

    # Closing all connections before passing to metadata migration. It's important to avoid any connections overflow.
    ro.conn.close()
    sf.conn.cursor().close()
    sf.conn.close()

    # Checking for errors when migrating tables.
    if len(error_tables):
        print("‼️ When migrating the tables into Snowflake, the following tables present some problems:")
        for error in error_tables:
            print(f" - {error[0]} | {error[1]}")
            print(f" ---> \t{error[3]}")

    meta_start = time.time()
    recreate_metadata_on_snowflake(sf_db,
                                   ddl_table=ddl_df,
                                   create_tables=False,
                                   logging=True)
    all_times_list.append(time.time() - meta_start)

    return [f"Execution Time: {round(sum(all_times_list), 2)}s", error_tables]


def migrate_metadata_from_redshift(rs_db: str,
                                   sf_db: str,
                                   schemas_list: Optional[List] = None,
                                   avoid_schemas_list: Optional[List[str]] = None,
                                   tables_list: Optional[List] = None,
                                   avoid_tables_list: Optional[List[str]] = None,
                                   create_tables: bool = False,
                                   logging: bool = True,
                                   verbose: bool = True,
                                   schema_migration_dict: Optional[dict] = None):
    """
    When Data is migrated, the metadata isn't sent with. So we have to send it separately.
    :param rs_db: Redshift database name.
    :param sf_db: Snowflake database name.
    :param schemas_list: List of schemas to be migrated.
    :param avoid_schemas_list: List of schemas not to be included.
    :param tables_list: List of tables to be migrated.
    :param avoid_tables_list: List of tables not to be included.
    :param create_tables: If the tables being migrated don't exist beforehand, they must be created.
    :param logging: Since SQL Syntax errors can be pretty hard to understand and debug, we can set logging
                          to True in order to have the problematic queries written down into the query_log_errors.txt
                          file.
    :param verbose: See all the DDL Queries being read from the redshift tables.
    :param schema_migration_dict: If the migration happens to be between schemas with different names,
                                                  we can set this config as a dictionary.
                                                  - For example:
                                                        If we want to migrate the metadata from schema1 in Redshift
                                                        into schema2 in Snowflake, we can set this relation as:
                                                        >>> schema_migration_dict = {schema1: schema2}.
    :return:
    """
    print("🦆 Starting the metadata migration process | Redshift -> Snowflake")
    ro = RedshiftOperator(database=rs_db)
    ddl_df = ro.get_DDL(schema_names=schemas_list,
                        avoid_schema_names=avoid_schemas_list,
                        table_names=tables_list,
                        avoid_table_names=avoid_tables_list,
                        verbose=verbose)
    ddl_df.fillna("", inplace=True)

    if schema_migration_dict is not None:
        ddl_df.replace(schema_migration_dict, regex=True, inplace=True)
    if logging:
        if os.path.exists("query_log_errors.txt"):
            os.remove("query_log_errors.txt")

    recreate_metadata_on_snowflake(sf_db,
                                   ddl_table=ddl_df,
                                   create_tables=create_tables,
                                   logging=True)


def recreate_metadata_on_snowflake(database: str,
                                   ddl_table: pd.DataFrame,
                                   create_tables: bool = False,
                                   logging: bool = True):
    """
    Recreate all metadata in Snowflake based on a ddl_table containing all the metadata information.
    :param database: Snowflake database name.
    :param ddl_table: The ddl_table is retrieved from the Redshift Operator.
    :param create_tables: Boolean value which indicates if we want to create the tables as well or not.
    :param logging: Boolean value which indicates if we want to log the problematic queries in a
    query_log_errors.txt file.
    :return:
    """
    print("💎 Launching Metadata Migration...\n")
    sf = SnowflakeOperator(snowflake_database=database.upper())
    ddl_model = ddl_table.copy()
    if create_tables:
        print("🖼 Creating tables if they don't already exist...")
        # Some of these corrections below must be done because 'year', 'level', 'region', 'names' are SQL Syntax Names
        # and AWS parse them as strings when creating the column names. However, Snowflake parses it otherwise because
        # it can distinguish the column names and the SQL Variables as different things.
        ddl_model['create_query'] = ddl_model['create_query'].str.replace("CREATE TABLE IF NOT EXISTS",
                                                                          "CREATE OR REPLACE TABLE")
        ddl_model["create_query"] = correct_sql_system_variables_syntax(ddl_model, "create_query")
        sf.execute_metadata_query(ddl_model.create_query.values, logging=logging, correct_syntax=True)

    print("🏷 Migrating Table Descriptions...")
    sf.execute_metadata_query(ddl_model.table_description.values, logging=logging)

    print("🏷 Migrating Columns Descriptions...")
    ddl_model["columns_description"] = correct_sql_system_variables_syntax(ddl_model, "columns_description")
    sf.execute_metadata_query(ddl_model.columns_description.values, logging=logging)

    print("🔑 Migrating Primary Keys...")
    sf.execute_key_query(ddl_model, key="primary", logging=logging)

    print("🔑 Migrating Unique Keys...")
    sf.execute_key_query(ddl_model, key="unique", logging=logging)

    print("🔑 Migrating Foreign Keys...")
    sf.execute_metadata_query(ddl_model.foreign_keys.values, logging=logging)

    sf.conn.cursor().close()
    sf.conn.close()
    print("✅ All metadata have been migrated successfully!")


class SnowflakeOperator:
    def __init__(self,
                 snowflake_user=None,
                 snowflake_password=None,
                 snowflake_account=None,
                 snowflake_warehouse=None,
                 snowflake_role=None,
                 snowflake_database=None) -> None:

        self.snowflake_user = (
            os.environ.get("SNOWFLAKE_USER")
            if snowflake_user is None
            else snowflake_user.upper()
        )
        self.snowflake_password = (
            os.environ.get("SNOWFLAKE_PASSWORD")
            if snowflake_password is None
            else snowflake_password
        )
        self.snowflake_account = (
            os.environ.get("SNOWFLAKE_ACCOUNT")
            if snowflake_account is None
            else snowflake_account.upper()
        )
        self.snowflake_warehouse = (
            os.environ.get("SNOWFLAKE_WAREHOUSE")
            if snowflake_warehouse is None
            else snowflake_warehouse.upper()
        )
        self.snowflake_role = (
            os.environ.get("SNOWFLAKE_ROLE")
            if snowflake_role is None
            else snowflake_role.upper()
        )
        self.snowflake_database = (
            os.environ.get("SNOWFLAKE_DATABASE")
            if snowflake_database is None
            else snowflake_database.upper()
        )

        self.schema = None

        self.conn = snowflake.connector.connect(
            user=self.snowflake_user,
            password=self.snowflake_password,
            account=self.snowflake_account,
            warehouse=self.snowflake_warehouse,
            role=self.snowflake_role,
            database=self.snowflake_database,
        )

    def truncate(self, database, schema, table):
        sql = f"truncate table {database}.{schema}.{table};"
        self.conn.cursor().execute(sql)

    def send_table(self, df: pd.DataFrame, table_name: str, quotes: bool = False):
        self.conn.cursor().execute(f"USE DATABASE {self.snowflake_database.upper()};")

        # Search the amount of processor cores available on the computer.
        processor_cores = os.cpu_count()
        # Subtract 2 from all the available cores to parallelize the processing. It can't be lower than 4.
        cores_usage = processor_cores - 2 if processor_cores >= 6 else processor_cores
        # Setting a chunk size based on the size of the table.
        chunk_usage = None if df.__len__() < 5 * 10 ** 6 else int(df.__len__() / 3)

        if self.schema is None:
            raise ValueError("❌ Please, set a schema name to where the table should be sent: \n"
                             "\t\t Example: sf = SnowflakeOperator()\n"
                             "\t\t          sf.schema = 'schema_name'")
        else:
            success, nchunks, nrows, _ = write_pandas(conn=self.conn,
                                                      df=df,
                                                      table_name=table_name.upper(),
                                                      schema=self.schema.upper(),
                                                      database=self.snowflake_database.upper(),
                                                      auto_create_table=True,
                                                      overwrite=True,
                                                      chunk_size=chunk_usage,
                                                      quote_identifiers=quotes,
                                                      parallel=cores_usage)

    def get_table(self, table_name: str) -> pd.DataFrame:
        if self.schema is None:
            raise ValueError("❌ Please, set a schema name to where the table should be sent: \n"
                             "\t\t Example: sf = SnowflakeOperator()\n"
                             "\t\t          sf.schema = 'schema_name'")
        else:
            df_from_sf = self.conn.cursor().execute(
                f"SELECT * FROM {self.schema.upper()}.{table_name.upper()}"
            ).fetch_pandas_all()

        return df_from_sf

    def drop_old_tables(self, ddl_df: pd.DataFrame, schema_list: Optional[List[str]] = None):
        """
        It aims to synchronize the tables in Snowflake and Redshift by dropping the tables present in Snowflake but
        not in Redshift.
        :param ddl_df: DDL table listing all the tables with its schemas in Redshift.
        :param schema_list: If we want to pass a subset of schemas under the ddl datafrale we can define it here.
        """
        if schema_list:
            df__sf_tables = self.list_tables(schema_list=schema_list)
            ddl_df = ddl_df[ddl_df.schema_name.isin(schema_list)]
        else:
            schema_list = list(ddl_df["schema_name"].unique())
            df__sf_tables = self.list_tables(schema_list=schema_list)

        for schema in schema_list:
            sf_tables_list = df__sf_tables.loc[df__sf_tables['TABLE_SCHEMA'] == schema.upper(),
                                               'TABLE_NAME'].str.lower().values
            rs_tables_list = ddl_df.loc[ddl_df['schema_name'] == schema, 'table_name'].values

            tables_to_drop_list = list(set(sf_tables_list) - set(rs_tables_list))

            if tables_to_drop_list:
                print(f"Schema: {schema}")
                for table in tables_to_drop_list:
                    print(f"\t🗑 Dropping table {schema.upper()}.{table.upper()}...")
                    self.conn.cursor().execute(f"DROP TABLE IF EXISTS {schema.upper()}.{table.upper()}")
            else:
                print(f"👌 There's no tables to drop in {schema}.")

    def list_tables(self, schema_list: List[str]) -> pd.DataFrame:
        """
        It lists all the tables in Snowflake for a set of schemas.
        :param schema_list: List of schemas from where it will list the tables.
        :return: Dataframe returned by the lisitng query.
        """
        schema_list = [f"TABLE_SCHEMA = '{schema.upper()}'" for schema in schema_list]
        schema_list = ' OR '.join(schema_list)
        df_from_sf = self.conn.cursor().execute(
            f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE {schema_list} ;"
        ).fetch_pandas_all()

        return df_from_sf[["TABLE_SCHEMA", "TABLE_NAME"]]

    def copy_from_s3(self, s3_prefix, s3_file, database, schema, table,
                     quotes: bool = False, sep: str = "|", empty_field_as_null: bool = True,
                     null_if: List[str] = [""]):
        """
        The Snowflake SGBD has a SQL Command dedicated to copy tables directly from S3 into a schema.
        :param s3_prefix: Object prefix in s3.
        :param s3_file: Table name in s3.
        :param database: Database name in Snowflake.
        :param schema: Schema name in Snowflake.
        :param table: Table name in Snowflake.
        :return:
        """
        table_name = f'"{table.lower()}"' if quotes else table.upper()
        list_null_if = ", ".join(f"'{case}'" for case in null_if)
        self.conn.cursor().execute(
            f"""
            COPY INTO {database.upper()}.{schema.upper()}.{table_name}
            FROM s3://{os.environ.get("S3_DATAMART_BUCKET")}/{s3_prefix.lower()}/{s3_file.lower()}
            CREDENTIALS = (
            aws_key_id='{os.environ.get("AWS_ACCESS_KEY_ID")}',
            aws_secret_key='{os.environ.get("AWS_SECRET_ACCESS_KEY")}'
            )
            FILE_FORMAT=(field_delimiter='{sep}', SKIP_HEADER=1, FIELD_OPTIONALLY_ENCLOSED_BY='"', 
            NULL_IF=({list_null_if}), EMPTY_FIELD_AS_NULL = {str(empty_field_as_null).upper()}) 
            FORCE = TRUE;
            """
        )

    def correct_syntax(self, query: str, no_comments: bool = False) -> str:
        """
        Snowflake has a specific SQL syntax. If we get a SQL from another SGBD, we must firstly
        correct the syntax into the snowflake constraints.

        Args:
            query: String containing the SQL script.
            no_comments: If we want to keep the SQL comments as well or not. Recommended keeping as false.

        Returns: The same query but snowflake-compatible.
        """
        return convert_to_snowflake_syntax(query, no_comments)

    def execute_metadata_query(self, query: List[str], logging: bool = False, correct_syntax=False):
        """

        :param query:
        :param logging:
        :param correct_syntax:
        :return:
        """
        # The snowflake python API allows only one command per request. That's why we must split the input query into
        # a list of commands.
        # Also, snowflake has a specific SQL syntax. If we get a SQL from another database manager, we must firstly
        # correct the syntax into the snowflake constraints.
        if correct_syntax:
            queries_list = "".join(self.correct_syntax(command) for command in query if not re.match(r"^\s*$", command))
        else:
            queries_list = "".join(command for command in query if not re.match(r"^\s*$", command))
        queries_list = sqlparse.split(queries_list)

        for command in queries_list:
            try:
                self.conn.cursor().execute(f"{command.strip()};")
            except snowflake.connector.errors.ProgrammingError as e:
                if ("does not exist or not authorized" not in str(e)) or ("Empty SQL statement" not in str(e)):
                    if logging:
                        print(f"Problem found. Skipping command. Check the query_log_errors.txt for more details.")
                        log_file = open("query_log_errors.txt", "a+")
                        log_file.write(f"{command}\n")
                        print(e)
                        log_file.close()
                    else:
                        print(f"Problem found. Skipping command...")

    def execute_key_query(self, df: pd.DataFrame, key: str = "primary", logging: bool = False):
        for row in range(df.__len__()):
            if key == "primary":
                if df.iloc[row, 2] != "":
                    drop_key_query = f"ALTER TABLE {df.iloc[row, 0]}.{df.iloc[row, 1]} DROP PRIMARY KEY;"
                    key_query = f"ALTER TABLE {df.iloc[row, 0]}.{df.iloc[row, 1]} ADD PRIMARY KEY ({df.iloc[row, 2]});"
                    skip = False
                else:
                    skip = True

            elif key == "unique":
                if (df.iloc[row, 3] != "") and (df.iloc[row, 3] != df.iloc[row, 2]):
                    drop_key_query = f"ALTER TABLE {df.iloc[row, 0]}.{df.iloc[row, 1]} DROP UNIQUE ({df.iloc[row, 3]});"
                    key_query = f"ALTER TABLE {df.iloc[row, 0]}.{df.iloc[row, 1]} ADD UNIQUE ({df.iloc[row, 3]});"
                    skip = False
                else:
                    skip = True

            if not skip:
                try:
                    self.conn.cursor().execute(key_query)
                except snowflake.connector.errors.ProgrammingError as e:
                    if "already exists" in str(e):
                        self.conn.cursor().execute(drop_key_query)
                        self.conn.cursor().execute(key_query)
                    else:
                        if ("does not exist or not authorized" not in str(e)) or ("Empty SQL statement" not in str(e)):
                            if logging:
                                print(f"Problem found. Skipping command. "
                                      f"Check the query_log_errors.txt for more details.")
                                log_file = open("query_log_errors.txt", "a+")
                                log_file.write(f"{key_query}\n")
                                print(e)
                                log_file.close()
                            else:
                                print(f"Problem found. Skipping command...")
