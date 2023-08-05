import sys
import cx_Oracle
import datetime
import pandas as pd
import json
from bson import ObjectId
from bson import BSONSTR
from bson.codec_options import TypeCodec
from bson.codec_options import TypeRegistry
from bson.codec_options import CodecOptions
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


class OracleLOBCodec(TypeCodec):
    """
    Class to give support to mongodb to write objects cx_Oracle.LOB to bson strings. 
    """
    python_type = cx_Oracle.LOB    # the Python type acted upon by this type codec
    bson_type = BSONSTR   # the BSON type acted upon by this type codec

    def transform_python(self, value):
        """Function that transforms a custom type value into a type
        that BSON can encode."""
        return ''.join(value.read())

    def transform_bson(self, value):
        """Function that transforms a vanilla BSON type value into our
        custom type."""
        return value


# Creating codec and registry for mongodb
oraclelob_codec = OracleLOBCodec()
oracle_codec_options = CodecOptions(
    type_registry=TypeRegistry([oraclelob_codec]))


class JsonEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for oracle graph,
    all the customized stuff for encoding required for our endpoints
    can be handle in this class
    """

    def default(self, o):
        """
        Method to encodec custom types.
        """
        if isinstance(o, pd.Timestamp):
            return str(o)
        if isinstance(o, type(pd.NaT)):
            return None
        if isinstance(o, cx_Oracle.LOB):
            # https://cx-oracle.readthedocs.io/en/7.1/lob.html#LOB.read
            # WARNING: es posible que no lea todo el contenido,
            # de momento solo esta en pocos campos, no con contenidos muy largos.
            # ex: tabla RE_PROYECTO_INSTITUCION campo NRO_VALOR
            return ''.join(o.read())
        if isinstance(o, datetime.datetime):
            try:
                return datetime.datetime.strftime(o, format='%Y%m%d')
            except ValueError:
                return None
        if isinstance(o, pd.Series):
            return o.to_dict()
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# https://stackoverflow.com/questions/61404287/year-is-out-of-range-cx-oracle-python


def DateTimeConverter(value):
    """
    Return the date as string
    """
    return value


def OutputHandler(cursor, name, defaulttype, length, precision, scale):
    """
    Callback to parse cursor
    """
    if defaulttype == cx_Oracle.DATETIME:
        return cursor.var(cx_Oracle.STRING, arraysize=cursor.arraysize, outconverter=DateTimeConverter)
    # https://cx-oracle.readthedocs.io/en/latest/user_guide/lob_data.html#fetching-lobs-as-strings-and-bytes
    if defaulttype == cx_Oracle.DB_TYPE_CLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG, arraysize=cursor.arraysize)
    if defaulttype == cx_Oracle.DB_TYPE_BLOB:
        return cursor.var(cx_Oracle.DB_TYPE_LONG_RAW, arraysize=cursor.arraysize)


class Utils:
    """
    Utility class to handle some Oracle calls.
    """

    def __init__(self, user="system", password="colavudea", dburi="localhost:1521"):
        """
        Constructor to create an Utils Object
        Parameters:
        ----------
        user:str
            Oracle user, by default system, other users can be provided but be sure they have the right permissions in the DB.
        password:str
            Oracle pass for given user
        dburi:str
            Oracle db uri for connector, default "localhost:1521"

        """

        # https://blogs.oracle.com/opal/post/connecting-to-oracle-cloud-autonomous-database-through-sqlalchemy
        # https://docs.sqlalchemy.org/en/14/dialects/oracle.html#module-sqlalchemy.dialects.oracle.cx_oracle
        self.pool = cx_Oracle.SessionPool(user=user, password=password, dsn=dburi,
                                          min=2, max=5, increment=1, threaded=True, encoding="UTF-8", nencoding="UTF-8")

        self.engine = create_engine(
            "oracle://", creator=self.pool.acquire, poolclass=NullPool, implicit_returning=False, encoding="utf8")

    def request(self, query):
        """
        Perform a request to the Oracle with a query.

        Parameters:
        ----------
        query:str
            SQL query

        Returns:
        ----------
            dataframe with the results
        """
        # https://www.oracle.com/technical-resources/articles/embedded/vasiliev-python-concurrency.html
        # alternavite to evalute if the code above doesnt work
        # https://stackoverflow.com/questions/60887128/how-to-convert-sql-oracle-database-into-a-pandas-dataframe

        try:
            # df = pd.read_sql(query, con=self.connection)# this is deprecated, but it works fine (colunms name are all UPPERCASE)
            # df = pd.read_sql(query, con=self.engine)
            # https://docs.sqlalchemy.org/en/14/dialects/oracle.html#identifier-casings
            # df.columns = df.columns.str.upper()
            connection = self.pool.acquire()
            connection.outputtypehandler = OutputHandler
            cur = connection.cursor()
            cur.execute(
                "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
            cur.execute(query)
            rows = cur.fetchall()
            columns = [row[0] for row in cur.description]
            connection.close()
            df = pd.DataFrame(rows, columns=columns, dtype='object')
        except cx_Oracle.Error as error:
            print(error)
            # if someting is failing with the connector is better to quit.
            sys.exit(1)
        return df

    def get_keys(self, table, ktype="P"):
        """
        Returns the keys from the table on Oracle DB,

        Parameters:
        ----------
        table:str
            table on database ex: EN_PRODUCTO
        ktype:str
            key type, opetions P (Primary), F (Foreing)

        Returns:
        ---------
            pandas dataframe with key information
        """
        query = f"SELECT cols.table_name, cols.column_name, cols.position, cons.status, cons.owner \
                FROM all_constraints cons, all_cons_columns cols WHERE cols.table_name = '{table}' \
                AND cons.constraint_type = '{ktype}' AND cons.constraint_name = cols.constraint_name \
                AND cons.owner = cols.owner  ORDER BY cols.table_name, cols.position"
        return self.request(query)

    def get_tables(self, db):
        """
        Returns the names of the tables available for a given db name.

        Parameters:
        ----------
        db:str
            database name ex: UDEA_CV

        Returns:
        ----------
            list of tables names 
        """
        query = f"SELECT * FROM all_tables WHERE OWNER='{db}'"
        df = self.request(query)
        # https://docs.sqlalchemy.org/en/14/dialects/oracle.html#identifier-casing
        df.columns = df.columns.str.upper()
        return list(df["TABLE_NAME"].values)

    def get_db_data(self, db):
        """
        Returns a dictionary where the keys are the tables and the values the dataframes with the data.

        Parameters:
        ----------
        db:str
            Database name

        Returns:
        ----------
            Dictionary with all the data for the given database.
        """
        data = {}
        tables_names = self.get_tables(db)
        for table in tables_names:
            query = f"SELECT * FROM {db}.{table}"
            data[table] = self.request(query)
        return data

    def request_register(self, db, keys, table):
        """
        Returns a register for a given database(or table space), keys(Primary or foreing) and table from Oracle DB,

        Parameters:
        ----------
        db:str
            database for the table (or table space)
        keys:dict
            dictionary with primary or foreing keys and the values for the specific register.
        table:str
            table on database ex: EN_PRODUCTO

        Returns:
        ---------
            pandas dataframe with the information
        """
        query = f"SELECT * FROM {db}.{table} WHERE "
        for key in keys:
            query += f" {key}='{keys[key]}' AND"
        query = query[0:-3]
        req = self.request(query)
        return req


def is_dict(data):
    """
    function to check if data is a dict
    Parameters.
    ----------
    data:any
        it's suppose to be a dict

    Returns:
    ---------
        True if data is a dict otherwise False.
    """
    return isinstance(data, dict)


def is_list(data):
    """
    function to check if data is a list
    Parameters.
    ----------
    data:any
        it's suppose to be a list

    Returns:
    ---------
        True if data is a list otherwise False.
    """
    return isinstance(data, list)


def is_serie(data):
    """
    function to check if data is a pandas serie
    Parameters.
    ----------
    data:any
        it's suppose to be a pandas serie

    Returns:
    ---------
        True if data is a pandas serie otherwise False.
    """
    if is_dict(data) or is_list(data):
        return False
    return True


def section_exist(section, keys):
    """
    Section and subsections means alias in the graph fields,
    ex: the section in the json for EN_RED is network

    some tables doesn´t have sections in the json, for example RE_EVENTO_PROYECTO
    because it is a relationship table.

    Parameters.
    ----------
    section:str
        name of the table
    keys:list
        keys of the graph fields

    Returns:
    ---------
        True if section is found otherwise False.

    """
    for i in list(keys):
        if section == i:
            return True
    return False


def table_exists(fields, table):
    """
    Function to check if the table is in the graph field.

    Parameters.
    ----------
    fields:dict
        graph field with the map of aliases to create the json
    table:str
        name of the table

    Returns:
    ---------
        True if table is found otherwise False.
    """
    for i in list(fields.keys()):
        if table == i:
            return True
    return False


def parse_table(fields, table_name, data_row, filters_function=None):
    """
    Apply the filter and returns a dict,
    table fields to apply aliases to the table columns is not supported anymore,
    the names of the colunms are mapped to the json directly
    """
    data = {}
    # WARNING HERE; AT THE MOMENT I AM NOT PARSING FIELDS WITH ALIAS
    if table_exists(fields, table_name):
        if filters_function:
            data_row = filters_function(table_name, data_row)
        if is_dict(data_row):
            data = data_row
        else:
            data = data_row.to_dict()
    return data


def replace_graph_db_field(graph, value_old, value_new):
    """
    Allows to replace the filed "DB": "__VALUE__" for "DB": "__NEW_VALUE__"
    example for scienti:
        "DB": "__CVLAC__" for "DB": "UDEA_CV"
        "DB": "__GRUPLAC__" for "DB": "UDEA_GR"
        "DB": "__INSTITULAC__" for "DB": "UDEA_IN"

    Parameters:
    ----------
    graph:dict
        dictionary with the model
    value_old:str
        current value for "DB" field
    value_new:str
        new value for "DB" field

    Returns:
    ----------
        dict with the new graph with the field "DB" changed. 
    """
    graph_str = json.dumps(graph)
    graph_str = graph_str.replace(
        f'"DB": "{value_old}"', f'"DB": "{value_new}"')
    return json.loads(graph_str)

# def parse_table(fields,table_name,data_row,remove_nulls=True):
#    data={}
#    if table_exists(fields,table_name):
#        for field,alias in fields[table_name]["fields"].items():
#            if remove_nulls:
#                if data_row[field]:
#                    data[alias] = data_row[field]
#            else:
#                data[alias] = data_row[field]
#    return data
