from typing import Any, List, Dict, Set, Optional
from sqlalchemy import create_engine, inspect, text, Table, MetaData, Column, String
from .s3_operator import S3Operator
from ..pandas_manager import detect_aws_type, check_quality_table_names
import sqlparse
import json
import os
import re
import pandas as pd
import time
import connectorx as cx


def find_tables_by_column_name(column_name: str, database: Optional[str] = None, verbose: bool = False) -> pd.DataFrame:
    """
    For a given column name, this function will return a Dataframe containing the table name, the schema name and the
    column description of all the tables having this column.

    :param column_name: Name of the column to be searched.
    :param database: In which database this column should be searched.
    :param verbose: Details of the Redshift Operator call on the tables.
    :return:
    """
    print("📮 Connecting to Redshift...")
    db = os.environ.get("REDSHIFT_DB") if database is None else database
    ro = RedshiftOperator(database=db)

    print(f"📋 Getting tables w.r.t the column: {column_name}")
    df_by_column = ro.get_tables_by_column_name(col_name=column_name, verbose=verbose)

    ro.conn.close()
    print("✅ Process finished successfully!")

    return df_by_column


def send_metadata_to_redshift(table_name: str, database: Optional[str] = None, file_path: str = "table_metadata.json"):
    """
    Use this function to send the Table and Column Descriptions to Redshift. There is a standard JSON file which this
    function reads to retrieve all the mandatory descriptions.

    :param database: Redshift database name.
    :param file_path: Path to the JSON file.
    :return:
    """
    print(f"🎬 Reading the {file_path} ...")
    table_metadata_dict = json.loads(open(file_path).read())

    # print("📮 Connecting to Redshift...")
    db = os.environ.get("REDSHIFT_DB") if database is None else database
    ro = RedshiftOperator(database=db)

    source_track_df_list = []
    print("💿 Generating the SQL Query from the JSON...")
    list_tables = [table["name"] for table in table_metadata_dict["tables"]]
    try:
        table_id = list_tables.index(table_name)
        table = table_metadata_dict["tables"][table_id]
    except ValueError:
        print("❌ Exiting the process...")
        print(f"😰 The chosen table {table_name} is not present on the json file.")
        raise

    print(f"\t📌 {table['name']}:")
    for key, value in table['details'].items():
        if key == "description":
            if len(value) > 600:
                raise OverflowError(f"❌ {key.capitalize()} value for table {table['name']} is too long. "
                                    "Please, limit yourself to 600 chars max.")
        else:
            if len(value) > 400:
                raise OverflowError(f"❌ {key.capitalize()} value for table {table['name']} is too long. "
                                    "Please, limit yourself to 400 chars max.")

    print(f"\t\t🛠 Checking the metadata constraints...")
    table_description_str = f"Country: {table['details']['country']}\n\n" \
                            f"Table Schema: {table['details']['table_schema']}\n\n" \
                            f"Description: {table['details']['description']}\n\n" \
                            f"Source Name: {table['details']['source_name']}\n\n" \
                            f"Source UUID: {table['details']['source_uuid']}\n\n" \
                            f"Geographical Coverage: {table['details']['geographical_coverage']}\n\n" \
                            f"Geographical Granularity: {table['details']['geographical_granularity']}\n\n" \
                            f"Update Frequency: {table['details']['update_frequency']}\n\n" \
                            f"Last Update: {table['details']['last_update']}\n\n" \
                            f"Time Frame Coverage: {table['details']['time_coverage']}\n\n" \
                            f"Caveats: {table['details']['caveats']}\n\n" \
                            f"Additional Info: {table['details']['additional_information']}\n\n" \
                            f"Update Process: {table['details']['update_process']}\n\n" \
                            f"Import Format: {table['details']['file_import_format']}\n\n" \
                            f"Import Separator: {table['details']['file_import_separator']}\n\n" \
                            f"Table Type: {table['details']['table_type']}"

    table_description_sql = f"COMMENT ON table {table['details']['table_schema']}.{table['name']} " \
                            f"IS '{table_description_str}';"

    source_track_df_list.append(
        pd.DataFrame(
            data={"table_name": [table['name']],
                  "source_name": [table['details']['source_name']],
                  "source_link": [table['details']['source_link']]}
        ))

    columns_description_sql_lst = []
    for column in table["columns"]:
        sql = f"COMMENT ON column {table['details']['table_schema']}.{table['name']}.{column['name']} " \
              f"IS '{column['description']}';"
        columns_description_sql_lst.append(sql)
    columns_description_sql = "\n".join(columns_description_sql_lst)

    print("\t\t📋 Launching Table Description query...")
    ro.conn.execution_options(isolation_level="AUTOCOMMIT").execute(text(table_description_sql))

    print("\t\t🏛 Launching Columns Description query...")
    ro.conn.execution_options(isolation_level="AUTOCOMMIT").execute(text(columns_description_sql))

    print(f"\t\t🎉 Metadata insertion finished for {table['name']}")
    ro.conn.close()

    if database == "oip":
        print("🎁 Updating admin.global_sources_track_table table with the new source_link's.")
        new_sources_df = pd.concat(source_track_df_list, ignore_index=True)
        need_update_tables = new_sources_df.table_name.values

        global_sources_df = read_from_redshift(database="oip", method="auto",
                                               schema="admin", table="global_sources_track_table")

        tables_not_changed_df = global_sources_df[~global_sources_df.table_name.isin(need_update_tables)]
        updated_sources_df = pd.concat([tables_not_changed_df, new_sources_df], ignore_index=True)

        send_to_redshift(database="oip", schema="admin", table="global_sources_track_table",
                         df=updated_sources_df, check=True, send_metadata=False, drop=True)

    print("✅ Process finished successfully!")


def send_to_redshift(database: str,
                     schema: str,
                     table: str,
                     df: pd.DataFrame,
                     from_bucket: Optional[str] = None,
                     send_metadata: bool = True,
                     json_path: str = "table_metadata.json",
                     **kwargs: Any, ) -> None:
    """
    Function send_to_redshift.
    Use this function to send data to s3 bucket and redshift(using copy).

    Args:
        database (str): The name of database in redshift.
        schema(str): The name of schema in redshift&s3.
        table(str): The name of the table to save.
        df(pd.DataFrame): The dataframe to send.
        from_bucket(str): S3 Bucket from where the table will be retrieved.
        send_metadata(bool): It will call the send_metadata_to_redshift() function in order to retrieve the
                             metadata descriptions from the local json file.
        json_path(str): The path to the json file containing the Table and Columns Descriptions.

    Kwargs:
        check(bool): False by default. If True, check the column type and length is consistent as current table in
                     redshift.
        drop(bool): (Avoid to use!) False by default. If True, drop the datatable which exists already.
        debug(bool): False by default. If True, print debug information.
        dct_aws_type(Dict): Dictionary of column name as key, AWS as value. Generated by pandas_manager.detect_aws_type
                            by default, manuel input is possible)
        bucket(str): Datamart bucket by default. S3 Bucket name to save the data.


    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.send_to_redshift(database="my_database", schema="my_schema", table="my_table", df=my_dataframe, dct_aws_type=my_dct_aws_type)
    """
    # Check if the column names agree with the SQL standards. It must not have accented letters or any special
    # character.
    check_quality_table_names(table_name=table, df=df)

    so = S3Operator()
    if not from_bucket:
        if database == "staging":
            so.bucket = kwargs.get("bucket", os.environ.get("S3_BUCKET_DEV"))
            if so.bucket is None:
                raise ValueError("❌ Environment variable missing: S3_BUCKET_DEV")
        else:
            so.bucket = kwargs.get("bucket", os.environ.get("S3_BUCKET_DATAMART"))
            if so.bucket is None:
                raise ValueError("❌ Environment variable missing: S3_BUCKET_DATAMART")
    else:
        so.bucket = from_bucket

    ro = RedshiftOperator(database=database, debug=kwargs.get("debug", False))
    ro.schema = schema
    ro.table = table
    ro.aws_type = kwargs.get("dct_aws_type", detect_aws_type(df=df))

    if kwargs.get("drop") is True:
        ro.drop_from_s3_and_redshift(bucket=so.bucket)

    so.send_to_s3_obj(df=df, s3_file_path=os.path.join(schema, f"{table}.csv"), sep="|")
    ro.process_table(bucket=kwargs.get("bucket", so.bucket), sep="|", check=kwargs.get("check", False))

    if send_metadata:
        try:
            send_metadata_to_redshift(table_name=table, database=database, file_path=json_path)
        except ValueError:
            print(f"🔍 Please check if the name is correct or set send_metadata to false.")
            raise
        except FileNotFoundError:
            print(f"⁉️ The JSON file containing all metadata was not found. Please, either check if the "
                  f"file path passed is correct, or set send_metadata to False.")
            raise
        finally:
            ro.conn.close()


def read_from_redshift(database: str, method: str, **kwargs) -> pd.DataFrame:
    """
    Function read_from_redshift.
    Use this function to read data from redshift.

    Args:
        database(str): The name of database in redshift.
        method(str): Default "auto", retreive data with limit and select, or "sql" retreive data with sql query.
    Kwargs:
        schema(str): The name of schema in redshift.
        table(str): The name of the table in redshift.
        limit(int): The line limit to read. Default None.
        select(str): The content to select. Default "*".

        debug(bool): False by default. If True, print debug information.

    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.read_from_redshift(database="my_database", method="auto", schema="my_schema", table="my_table")
        >>> database_manager.read_from_redshift(database="my_database", method="sql", sql_query='SELECT * FROM my_schema.my_table')
    """
    ro = RedshiftOperator(database=database, debug=kwargs.get("debug", False))
    ro.schema = kwargs.get("schema")
    ro.table = kwargs.get("table")
    if method == "auto":
        df_from_redshift = ro.read_from_redshift(limit=kwargs.get("limit", None), select=kwargs.get("select", "*"))
    elif method == "sql":
        df_from_redshift = ro.read_sql_from_redshift(sql_query=kwargs.get("sql_query", None))
    else:
        raise ValueError(f"Unrecognized method: {method}")
    return df_from_redshift


class RedshiftOperator:
    """
    RedshiftOperator, build redshift connection, read data from or send data to redshift.

    Args:
        database (str): The database for connection.

    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> ro = database_manager.RedshiftOperator()
        >>> ro.read_from_redshift(schema="my_schema", table="my_table", limit=10)
    """

    def __init__(self,
                 database: str = os.environ.get("REDSHIFT_DB"), debug: bool = False) -> None:
        self.redshift_user = os.environ.get("REDSHIFT_USER")
        self.redshift_password = os.environ.get("REDSHIFT_PASSWORD")
        self.redshift_host = os.environ.get("REDSHIFT_HOST")
        self.redshift_database = database
        if database is None:
            raise ValueError(f"❌Input database not defined in .env")
        self.engine = create_engine(
            f"redshift+psycopg2://{self.redshift_user}:{self.redshift_password}@{self.redshift_host}:5439/{self.redshift_database}",
            echo=debug,
        )
        self.conn = self.engine.connect()
        self._schema = None
        self._table = None
        self._aws_type = dict()
        self.df_std_error = None
        self.s3_bucket = None
        self.ddl_table = None
        # Session = sessionmaker(bind=self.engine)
        # self.session = Session()

    """
        property
    """

    @property
    def schema(self) -> str:
        return self._schema

    @schema.setter
    def schema(self, schema: str) -> None:
        print(f"☑️Setting schema to {schema}")
        self._schema = schema

    @property
    def table(self) -> str:
        return self._table

    @table.setter
    def table(self, table: str) -> None:
        print(f"☑️Setting table to {table}")
        self._table = table

    @property
    def aws_type(self):
        return self._aws_type

    @aws_type.setter
    def aws_type(self, dct_aws_type: Dict) -> None:
        print(f"☑️Setting AWS type: {dct_aws_type}")
        self._aws_type = dct_aws_type

    """
        read method
    """

    def read_from_redshift(self, limit: bool = None, select: str = "*", method: str = "pandas") -> pd.DataFrame:
        sql_limit = limit if limit else "NULL"
        query = f"SELECT {select} FROM {self._schema}.{self._table} LIMIT {sql_limit}"
        if method == "pandas":
            df_result = pd.read_sql_query(query, self.engine)
        if method == "ctx":
            df_result = cx.read_sql(
                f"redshift+psycopg2://{self.redshift_user}:{self.redshift_password}@{self.redshift_host}:5439/{self.redshift_database}",
                query, partition_num=8, return_type="pandas", )
        return df_result

    def read_sql_from_redshift(self, sql_query: str) -> pd.DataFrame:
        df_result = pd.read_sql_query(sql_query, self.engine)
        return df_result

    """
         table oriented method
    """

    def detect_table(self, ddl=False) -> bool:
        inspect_engine = inspect(self.engine)
        if not ddl:
            table_exists = inspect_engine.has_table(schema=self._schema, table_name=self._table)
        else:
            table_exists = inspect_engine.has_table(schema="admin", table_name="v_generate_tbl_ddl")
        return table_exists

    def clean_table(self) -> None:
        self.conn.execute(f"TRUNCATE TABLE {self._schema}.{self._table}")

    def drop_table(self) -> None:
        metadata = MetaData()
        datatable = Table(self._table, metadata, schema=self._schema)
        datatable.drop(self.engine, checkfirst=False)

    def create_table(self) -> None:
        assert (self._aws_type is not None), f"❌ dct_aws_type is not defined when creating table!"
        print(f"🔁{self._schema}.{self._table} structure doesn't exist, creating...")
        metadata = MetaData()
        query_tuple = tuple(
            Column(column_name, aws_type)
            for column_name, aws_type in self._aws_type.items()
        )
        datatable = Table(self._table, metadata, *query_tuple, schema=self._schema)
        datatable.create(self.engine, checkfirst=True)
        print(f"🏗Table Structure Created!")

    def get_current_structure(self) -> List:
        print(f"❗️{self._schema}.{self._table} structure exists, retrieving current structure...")
        get_current_len_query = f"""
        SELECT table_schema, table_name, column_name, data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_schema = '{self._schema}'
        AND table_name = '{self._table}'
        AND data_type = 'character varying'
        ORDER BY table_name;
        """
        df_current_structure = self.conn.execute(get_current_len_query)
        lst_current_structure = [(row[2], row[4]) for row in df_current_structure]
        return lst_current_structure

    def check_structure_consistency(self) -> Set:
        assert (self._aws_type is not None), f"❌ dct_aws_type is not defined when checking consistency!"
        # check varchar type
        lst_current_structure = self.get_current_structure()
        lst_new_structure = [(column_name, aws_type.length)
                             for column_name, aws_type in self._aws_type.items()
                             if isinstance(aws_type, String)]
        new_varchar = set(lst_new_structure) - set(lst_current_structure)
        return new_varchar

    def update_structure(self, iter_new_structure: Set) -> None:
        print(f"⚠️There are some columns need update: {iter_new_structure}")
        self.clean_table()
        for column, new_len in iter_new_structure:
            update_query = f"""
            ALTER TABLE "{self._schema}"."{self._table}"
            ALTER COLUMN "{column}" TYPE varchar({new_len});
            """
            self.conn.execution_options(isolation_level="AUTOCOMMIT").execute(update_query)
        print(f"✨Table Structure Updated!")

    def copy_from_s3(self,
                     bucket: str,
                     prefix: str,
                     s3_table: str,
                     sep: str,
                     redshift_schema: str,
                     redshift_table: str) -> None:
        s3_file_path = os.path.join(bucket, prefix, f"{s3_table}.csv")
        query = f"""
        COPY {redshift_schema}.{redshift_table} 
        FROM 's3://{s3_file_path}' 
        WITH CREDENTIALS 'aws_access_key_id={os.environ.get('AWS_ACCESS_KEY_ID')};aws_secret_access_key={os.environ.get('AWS_SECRET_ACCESS_KEY')}'
        REGION '{os.environ.get('AWS_DEFAULT_REGION')}'
        DELIMITER '{sep}'
        REMOVEQUOTES
        IGNOREHEADER 1
        """
        result = self.conn.execution_options(autocommit=True).execute(query)
        result.close()
        print(f"🥳Table is copied to redshift from S3.\n")

    def load_std_error(self) -> None:
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM stl_load_errors"))
            self.df_std_error = pd.DataFrame(result, columns=["userid", "slice", "tbl", "starttime", "session",
                                                              "query", "filename", "line_number", "colname", "type",
                                                              "col_length", "position", "raw_line", "raw_field_value",
                                                              "err_code", "err_reason", "is_partial", "start_offset"]) \
                .sort_values(by=["starttime"], ascending=[False])

    """
      summary method
    """

    def process_table(self, bucket: str, sep: str, check: bool = False) -> None:
        table_exists = self.detect_table()
        if table_exists and (check is False):
            pass
        elif table_exists and (check is True):
            iter_new_structure = self.check_structure_consistency()
            if len(iter_new_structure) > 0:
                self.update_structure(iter_new_structure=iter_new_structure)
            else:
                print(f"🥳Table Structure is consistent!")
        else:
            self.create_table()
        self.clean_table()

        self.copy_from_s3(bucket=bucket, prefix=self._schema, s3_table=self._table, sep=sep,
                          redshift_schema=self._schema, redshift_table=self._table)

    def drop_from_s3_and_redshift(self, bucket: str = os.environ.get("S3_BUCKET_DEV")):
        """
        If we want to drop a table from both Redshift and S3 at once, we can simply call this function.
        :param bucket: Bucket name on s3 where the object is placed.
        :return:
        """
        so = S3Operator()
        so.bucket = bucket
        so.prefix = self.schema

        if self.detect_table():
            print("✂️ Dropping Redshift Table...")
            self.drop_table()
        else:
            print(f"\t🔍 Redshift | Table {self.table} doesn't exist on {self.schema}. Thus, no need to drop...")

        if so.table_exists(self.table):
            print("✂️ Removing S3 Object...")
            so.remove_object(self.table)
        else:
            print(f"\t🔍 S3 | Object {self.table}.csv doesn't exist on prefix {self.schema}. Thus, no need to drop...")

    def generate_DDL(self):
        """
        This function launches the query present in v_generate_tbl_ddl.sql to assemble the DDL queries from all the
        redshift tables into a single one.
        :return:
        """
        query = (open(os.path.join(os.path.dirname(__file__), "../sql_utils/v_generate_tbl_ddl.sql"), "r")
                 .read()
                 .replace("%", "%%"))
        self.conn.execution_options(isolation_level="AUTOCOMMIT").execute(text(query))

    def get_DDL(self,
                schema_names: Optional[List[str]] = None,
                avoid_schema_names: Optional[List[str]] = None,
                table_names: Optional[List[str]] = None,
                avoid_table_names: Optional[List[str]] = None,
                verbose: bool = True,
                output_to: Optional[str] = None):
        """
        This function makes a Redshift request to retrieve the v_generate_tbl_ddl table responsible for
        stocking the ddl queries from all the redshift tables.

        :param schema_names: List os schemas to be considered if customization is needed.
        :param avoid_schema_names: List of schemas to be excluded if any.
        :param table_names: List of tables to be considered if customization is needed.
        :param avoid_table_names:List of tables to be excluded if any.
        :param verbose: Print details.
        :param output_to: If we want to export this table somewhere, tha path must be passed here.
        :return:
        """
        # Generate the DDL table.
        self.generate_DDL()
        time.sleep(2)  # Allow a little of time for the query to finish executing.

        if avoid_schema_names is None:
            avoid_schema_names = ["public", "pv_reference", "platform", "pv_intermediary_tables", "pg_catalog",
                                  "information_schema"]

        print("⏳ Generating the DDL Table. It can take a while...")
        query = f"select * from admin.v_generate_tbl_ddl"
        result = self.conn.execute(text(query)).all()
        if not schema_names:
            schema_names = list(set([record.schemaname for record in result]))

        dfs = []
        for schema in set(schema_names).difference(avoid_schema_names):
            if verbose:
                print(schema)
            if not table_names:
                table_names_list = list(set([record.tablename for record in result if record.schemaname == schema]))
                if avoid_table_names:  # Exclude the tables if any.
                    table_names_list = set(table_names_list).difference(avoid_table_names)
            else:
                # Intercession between both sets.
                table_names_list = list(set(table_names) &
                                    set([record.tablename for record in result if record.schemaname == schema]))

            for table in table_names_list:
                if verbose:
                    print(f" - {table}")
                corrected_query = ""
                for record in result:
                    if (record.schemaname == schema) and (record.tablename == table):
                        line = (record.ddl.replace(" ", " ").replace("'\"", "'").replace("\"'", "'").replace('""', '"'))
                        if line.count("'") > 2:
                            line = "'".join([line.split("'")[0], "''".join(line.split("'")[1:-1]), line.split("'")[-1]])
                        corrected_query += f"{line}\n"

                corrected_query = corrected_query.replace(".year ", '."year" ') \
                    .replace(".level ", '."level" ') \
                    .replace(".region ", '."region" ') \
                    .replace(".names ", '."names" ') \
                    .replace(".type ", '."type" ') \
                    .replace(".role ", '."role" ') \
                    .replace(".provider ", '."provider" ') \
                    .replace(".location ", '."location" ') \
                    .replace(".index ", '."index" ')

                corrected_query = sqlparse.split(corrected_query)

                create_sql = "".join([statement for statement in corrected_query if
                                      "CREATE TABLE IF NOT EXISTS".lower() in statement.lower()])
                create_sql = ";\n".join(create_sql.split(";\n")[1:])
                primary_key = (
                    re.findall(r",PRIMARY KEY \((\w+)\)", create_sql)[-1]
                    if len(re.findall(r",PRIMARY KEY \((\w+)\)", create_sql)) > 0
                    else ""
                )
                unique_key = (
                    re.findall(r",UNIQUE \((\w+)\)", create_sql)[-1]
                    if len(re.findall(r",UNIQUE \((\w+)\)", create_sql)) > 0
                    else ""
                )
                comment_table_sql = "".join(
                    [
                        statement
                        for statement in corrected_query
                        if "COMMENT ON table".lower() in statement.lower()
                    ]
                )
                comment_columns_sql = "\n".join(
                    [
                        statement
                        for statement in corrected_query
                        if "COMMENT ON column".lower() in statement.lower()
                    ]
                )
                foreign_key_sql = "\n".join(
                    [
                        statement
                        for statement in corrected_query
                        if "FOREIGN KEY".lower() in statement.lower()
                    ]
                )

                # Check if the column names agree with the SQL standards. It must not have accented letters or any special character.
                # For some reason, when we retrieve the DDL from Redshift, it gives the CREATE TABLE Sql correctly but not
                # the COMMENT ON Sql script. Whenever a column name has a non-ASCII name, we must parse it as string (under quotes).
                # This script down below corrects the COMMENT ON string with the quotes notation.
                sql_columns = re.findall(r"\n\t[,]*\"([.\S]+)\"\s+", create_sql)
                string_check = re.compile(r"[@\-!#$%^&*+()<>?/\|}{~:]")
                for var in sql_columns:
                    if not var.isascii() or (string_check.search(var) is not None):
                        comment_columns_sql = comment_columns_sql.replace(
                            f".{var} IS", f'."{var}" IS'
                        )

                df = pd.DataFrame(
                    {
                        "schema_name": schema,
                        "table_name": table,
                        "primary_key": primary_key,
                        "unique_key": unique_key,
                        "create_query": create_sql,
                        "table_description": comment_table_sql.strip(),
                        "columns_description": comment_columns_sql.strip(),
                        "foreign_keys": foreign_key_sql.strip(),
                    },
                    index=[1],
                )
                dfs.append(df)

        print("DDL Table generated!")
        self.ddl_table = pd.concat(dfs, ignore_index=True).reset_index(drop=True)
        self.ddl_table.sort_values(["schema_name", "table_name"], ascending=[1, 1], ignore_index=True, inplace=True)

        if output_to is not None:
            print("Exporting table to folder.")
            if not os.path.exists(output_to):
                os.makedirs(output_to)
            self.ddl_table.to_csv(os.path.join(output_to, "ddl_model.txt"), sep="\t", encoding="utf-8", index=False)
            print(f"🥳DDL now is available in {output_to}/ddl_model.txt\n")

        return self.ddl_table

    def get_tables_by_column_name(self, col_name: str, verbose=False) -> pd.DataFrame:
        """
        For a given column name, this function will return a Dataframe containing the table name, the schema name
        and the column description of all the tables having this column.
        :param col_name: Name of the column to be searched.
        :param verbose: Details of the Redshift Operator call on the tables.
        :return:
        """
        if self.ddl_table is None:
            self.get_DDL(verbose=verbose)

        df_filtered = self.ddl_table[self.ddl_table.create_query.str.contains(f'[\s,"]{col_name}[\s"]')]

        schema_names_lst = df_filtered["schema_name"].values
        table_names_lst = df_filtered["table_name"].values
        columns_description = df_filtered["columns_description"].apply(
            lambda x: re.findall(f"\\.{col_name} IS '(.*)';", x)[0] if
            len(re.findall(f"\\.{col_name} IS '(.*)';", x)) > 0 else "").values

        data = {'schema_name': schema_names_lst, 'table_name': table_names_lst,
                'column_name': col_name, 'column_description': columns_description}

        return pd.DataFrame(data=data)
