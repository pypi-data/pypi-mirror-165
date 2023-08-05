from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from pydatafabric.vault_utils import get_secrets
from pydatafabric.gcp import get_bigquery_client
import pandas as pd
import cx_Oracle

GCP_PROJECT = "smart-ruler-304409"
TEMP_DATASET = "temp_1d"
ORACLE_SECRET = None
DCRYPTO_LIST = pd.DataFrame([])


def set_oracle_secret(secret):
    global ORACLE_SECRET
    ORACLE_SECRET = secret


def set_dcrypto_list(dcrypto_list):
    global DCRYPTO_LIST
    DCRYPTO_LIST = dcrypto_list


def get_enc_type(owner, table_name, column_name):
    global DCRYPTO_LIST
    enc_type = None
    enc_list = None
    try:
        enc_list = DCRYPTO_LIST.query(
            "(OWNER==@owner) and (TABLE_NAME==@table_name) and (COLUMN_NAME==@column_name)"
        )[["ENC_TYPE"]]
        if len(enc_list.index) == 1:
            enc_type = enc_list.iloc[0]["ENC_TYPE"]
    except NameError:
        enc_type = None

    return enc_type


def get_enc_list(owner, table_name):
    global DCRYPTO_LIST
    try:
        enc_list = DCRYPTO_LIST.query("(OWNER==@owner) and (TABLE_NAME==@table_name)")[
            ["COLUMN_NAME", "ENC_TYPE"]
        ]
    except NameError:
        enc_list = None

    return enc_list


def get_oracle_connection():
    connection = cx_Oracle.connect(
        user=ORACLE_SECRET["user"],
        password=ORACLE_SECRET["password"],
        dsn=ORACLE_SECRET["cx_url"],
        encoding=ORACLE_SECRET["encoding"],
        nencoding=ORACLE_SECRET["nencoding"],
    )

    return connection


def get_oracle_schema(owner, table_name):
    schema_sql = """
    SELECT A.OWNER AS SCHEMA_NAME, A.TABLE_NAME AS TABLE_NAME, E.COMMENTS AS TABLE_COMMENTS,
        CASE WHEN C.COLUMN_NAME IS NOT NULL THEN '1' ELSE NULL END AS IS_PK,
        B.COLUMN_NAME AS COLUMN_NAME, D.COMMENTS AS COLUMN_COMMENTS, B.COLUMN_ID AS POSITION,
        B.DATA_TYPE AS DATA_TYPE_NAME, B.NULLABLE AS IS_NULLABLE,
        B.DATA_LENGTH AS LENGTH,
        B.DATA_SCALE AS SCALE, B.DATA_PRECISION AS PRECISION
    FROM ALL_TABLES A
        INNER JOIN ALL_TAB_COLUMNS B
        ON  A.TABLE_NAME = B.TABLE_NAME
        INNER JOIN ALL_COL_COMMENTS D
        ON B.TABLE_NAME = D.TABLE_NAME
        AND B.COLUMN_NAME = D.COLUMN_NAME
        LEFT JOIN (
            SELECT A.TABLE_NAME, B.COLUMN_NAME
                FROM ALL_CONSTRAINTS A
                    INNER JOIN ALL_CONS_COLUMNS B
                    ON A.CONSTRAINT_NAME = B.CONSTRAINT_NAME
                    AND A.CONSTRAINT_TYPE = 'P'
        ) C
        ON B.TABLE_NAME = C.TABLE_NAME
        AND B.COLUMN_NAME = C.COLUMN_NAME
        INNER JOIN ALL_TAB_COMMENTS E
        ON  A.TABLE_NAME = E.TABLE_NAME
    WHERE A.OWNER IN (:owner)
    AND A.TABLE_NAME = :table_name
    ORDER BY A.TABLE_NAME, B.COLUMN_ID
    """

    bind_param = dict(owner=owner.upper(), table_name=table_name.upper())
    oracle_schema = oracle_to_pandas(
        owner=owner, table_name=table_name, sql=schema_sql, bind_param=bind_param
    )

    return oracle_schema


def output_type_handler(cursor, name, default_type, size, precision, scale):
    import datetime as dt
    import decimal as dc

    if default_type in (
        cx_Oracle.DB_TYPE_VARCHAR,
        cx_Oracle.DB_TYPE_CHAR,
        cx_Oracle.DB_TYPE_NCHAR,
        cx_Oracle.DB_TYPE_NVARCHAR,
    ):
        return cursor.var(str, arraysize=cursor.arraysize, bypass_decode=True)
    elif default_type == cx_Oracle.DB_TYPE_CLOB:
        return cursor.var(
            cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize, bypass_decode=True
        )
    elif default_type in (
        cx_Oracle.DB_TYPE_DATE,
        cx_Oracle.DB_TYPE_TIMESTAMP,
        cx_Oracle.DB_TYPE_TIMESTAMP_TZ,
        cx_Oracle.DB_TYPE_TIMESTAMP_LTZ,
    ):
        return cursor.var(str, arraysize=cursor.arraysize, bypass_decode=True)
    elif default_type == cx_Oracle.DB_TYPE_NUMBER:
        return cursor.var(dc.Decimal, arraysize=cursor.arraysize, bypass_decode=False)


def make_dict_factory(cursor):
    columnNames = [row[0] for row in cursor.description]

    def createRow(*args):
        return dict(zip(columnNames, args))

    return createRow


def getDefault(val, default):
    return val if val is not None else default


def convert_oracle_to_bigquery_schema(owner, table_name, partition_field=None):
    oracle_schema = get_oracle_schema(owner, table_name)
    schema = []
    if partition_field and isinstance(partition_field, bigquery.SchemaField):
        schema.append(partition_field)

    for i in range(len(oracle_schema)):
        row = oracle_schema.iloc[i]
        description = getDefault(row["column_comments"], "")
        column = row["column_name"].lower()
        oc_type = row["data_type_name"]
        nullable = row["is_nullable"]
        scale = getDefault(row["scale"], "")
        precision = getDefault(row["precision"], "")
        length = row["length"]

        bq_type = "STRING"
        if oc_type in ("VARCHAR2", "CHAR", "NVARCHAR2", "CLOB"):
            bq_type = "STRING"
        elif oc_type == "NUMBER":
            if precision and precision >= 0:
                if scale == 0:
                    if precision < 9:
                        bq_type = "INTEGER"
                    elif precision >= 9 and precision < 22:
                        bq_type = "NUMERIC"
                    elif precision >= 22:
                        bq_type = "BIGNUMERIC"
                elif scale > 0:
                    bq_type = "FLOAT"
            else:
                bq_type = "NUMERIC"
        elif oc_type == "LONG":
            bq_type = "NUMERIC"
        elif oc_type == "DATE":
            bq_type = "STRING"
        elif oc_type.startswith("TIMESTAMP"):
            bq_type = "DATETIME"

        mode = "REQUIRED" if nullable == "N" else "NULLABLE"

        schema.append(
            bigquery.SchemaField(column, bq_type, mode=mode, description=description)
        )

    return schema


def decode_byte(objs, encode_type="cp949"):
    if type(objs) is list:
        result = objs
        for i in range(len(result)):
            for col in result[i].keys():
                if isinstance(result[i][col], bytes):
                    result[i][col] = result[i][col].decode(encoding=encode_type)
        return result
    elif type(objs) is tuple:
        temp = list(objs)
        result = []
        for item in temp:
            if isinstance(item, bytes):
                try:
                    result.append(item.decode(encoding=encode_type))
                except UnicodeDecodeError:
                    lens = len(item) - 1
                    result.append(item[:lens].decode(encoding=encode_type))
            else:
                result.append(item)
        return result
    else:
        return objs


def decrypt_columns(dataframe, enc_list, columns):
    import hashlib

    result = dataframe

    for row in enc_list.itertuples():
        enc_column_name = row.COLUMN_NAME

        if enc_column_name in columns:
            result[enc_column_name] = result[enc_column_name].apply(
                lambda x: hashlib.sha256(x.encode()).hexdigest()
                if (pd.notnull(x))
                else x
            )

    return result


def oracle_fetchall_to_pandas(
    owner, table_name, sql=None, bind_param=None, enc_list=None
):

    result = None

    if sql is None:
        sql = "SELECT * FROM {}".format(table_name)
    else:
        sql = sql

    connection = get_oracle_connection()
    cursor = connection.cursor()
    cursor.outputtypehandler = output_type_handler
    cursor.execute(
        "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' NLS_TIMESTAMP_TZ_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF3'"
    )

    if bind_param is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, bind_param)

    columnNames = [row[0] for row in cursor.description]
    cursor.rowfactory = make_dict_factory(cursor)
    result = cursor.fetchall()
    result = decode_byte(result)

    result = pd.DataFrame(data=result)

    if enc_list:
        result = decrypt_columns(result, enc_list, columnNames)

    cursor.close()
    connection.close()

    return result


def oracle_to_pandas(owner, table_name, sql=None, bind_param=None, enc_list=None):

    result = None

    if sql is None:
        sql = "SELECT * FROM {}".format(table_name)
    else:
        sql = sql

    connection = get_oracle_connection()
    cursor = connection.cursor()
    cursor.outputtypehandler = output_type_handler
    cursor.execute(
        "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' NLS_TIMESTAMP_TZ_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF3'"
    )

    if bind_param is None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, bind_param)

    columnNames = [row[0] for row in cursor.description]
    result = map(lambda x: decode_byte(x), cursor)

    result = pd.DataFrame(data=result, columns=columnNames)

    if enc_list:
        result = decrypt_columns(result, enc_list, columnNames)

    result = result.rename(columns=str.lower)
    cursor.close()
    connection.close()

    return result


def bq_dataset_exists(dataset, project=GCP_PROJECT):
    try:
        bq = get_bigquery_client(project=project)
        dataset = bq.get_dataset(dataset)
        bq.close()
    except NotFound:
        return False
    return True


def create_bq_table_with_oracle_schema(
    owner,
    oracle_table,
    bq_dataset,
    bq_project=GCP_PROJECT,
    bq_table=None,
    partition_type=None,
    partition_field=None,
):
    if not bq_dataset_exists(bq_dataset, bq_project):
        print("Not Exists Dataset: {}".format(bq_dataset))
        return False

    bq_table_name = bq_table if bq_table else oracle_table.lower()

    if partition_field:
        partition_field_schema = bigquery.SchemaField(
            partition_field, "DATE", mode="REQUIRED", description="파티션 컬럼"
        )
    schema = convert_oracle_to_bigquery_schema(
        owner=owner, table_name=oracle_table, partition_field=partition_field_schema
    )

    dataset_ref = bigquery.DatasetReference(bq_project, bq_dataset)
    table_ref = dataset_ref.table(bq_table_name)
    table = bigquery.Table(table_ref, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field=partition_field,
    )

    bq = get_bigquery_client(project=bq_project)

    result = bq.create_table(table, exists_ok=True)
    print(
        "Created table {}, partitioned on column {}".format(
            result.table_id, result.time_partitioning.field
        )
    )

    bq.close()


def get_bigquery_load_job_config(
    schema, write_disposition, partition_type=None, partition_field=None
):

    job_config = bigquery.LoadJobConfig()
    job_config.schema = schema
    job_config.write_disposition = write_disposition
    job_config.create_disposition = "CREATE_IF_NEEDED"
    job_config.source_format = bigquery.SourceFormat.PARQUET
    job_config.autodetect = False

    if partition_type and partition_field:
        job_config.time_partitioning = bigquery.TimePartitioning(
            type_=partition_type, field=partition_field
        )

    return job_config


def generate_oracle_select_query(owner, table_name, where=None):
    oracle_schema = get_oracle_schema(owner, table_name)[
        ["schema_name", "table_name", "column_name", "data_type_name"]
    ]

    if len(oracle_schema.index) == 0:
        return False

    col_list = []
    table = ""

    for idx, row in oracle_schema.iterrows():
        table = row["table_name"].strip()
        column = row["column_name"].strip()
        # schema = row['schema_name'].strip()
        # oc_type = row['data_type_name'].strip()

        enc_type = get_enc_type(owner, table, column)
        if enc_type == "AES":
            col_list.append(f"AES.DEC({column}, 'emrt') AS {column}")
        elif enc_type == "CUB":
            col_list.append(f"XX1.DEC_VARCHAR2_SEL({column}, 10, 'SSNF') AS {column}")
        else:
            col_list.append(column)

    query = "SELECT " + ", ".join(col_list) + " FROM " + owner + "." + table

    if where:
        query += f" WHERE {where}"

    return query


def oracle_to_bq_overwrite_table(
    owner,
    table,
    dataset,
    bq_table=None,
    bq_project=GCP_PROJECT,
    partition_column=None,
    partition_type=None,
    partition_field=None,
    query=None,
):
    bq_table = bq_table if bq_table is not None else table.lower()
    query = query if query is not None else generate_oracle_select_query(owner, table)
    pdf = oracle_to_pandas(owner, table, sql=query)

    schema = ""
    if partition_column and partition_field:
        pdf[partition_field] = pd.to_datetime(
            pdf[partition_column.lower()], format="%Y-%m-%d %H:%M:%S"
        ).dt.date
        partition_schema_field = bigquery.SchemaField(
            partition_field, "DATE", mode="REQUIRED", description="파티션 컬럼"
        )
        schema = convert_oracle_to_bigquery_schema(owner, table, partition_schema_field)
    else:
        schema = convert_oracle_to_bigquery_schema(owner, table)

    if schema:
        bq = get_bigquery_client(project=bq_project)
        t_ref = bigquery.TableReference(
            bigquery.DatasetReference(bq_project, dataset), bq_table
        )
        jc = get_bigquery_load_job_config(
            schema, "WRITE_TRUNCATE", partition_type, partition_field
        )
        j = bq.load_table_from_dataframe(pdf, t_ref, job_config=jc)
        j.result()

        bq.close()
