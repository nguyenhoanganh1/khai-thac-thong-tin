from datetime import date, datetime
from sqlite3 import Row

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


orientdb_properties = {
    "user": "root",
    "password": "admin",
    "port": "2424",
    "url": "jdbc:orient:remote:localhost/demo",
    "driver": "com.orientechnologies.orient.jdbc.OrientJdbcDriver"
}

class SparkConfig:
    __metaclass__ = Singleton

    def load_class_data(self, class_name):
        custom_schema = StructType([
            StructField("id", IntegerType(), True),
            StructField("name", StringType(), True),
        ])

        # Read data from OrientDB into a DataFrame
        session = self.spark_master_session()
        session.read \
            .schema(custom_schema) \
            .option("spark.orientdb.connection.mode", "document") \
            .option("spark.orientdb.connection.uri", "remote:localhost/demo") \
            .option("spark.orientdb.connection.class", "users") \
            .option("spark.orientdb.connection.port", orientdb_properties["port"]) \
            .option("spark.orientdb.connection.username", orientdb_properties["user"]) \
            .option("spark.orientdb.connection.password", orientdb_properties["password"]) \
            .option("spark.orientdb.connection.query", f"select * from {class_name}") \
            .option("inferSchema", "true") \
            .load() \
            .show()


    def spark_session(self):
        return SparkSession.builder.getOrCreate()

    def spark_master_session(self):
        return SparkSession.builder.master("local[*]") \
            .appName("SparkByExample") \
            .config("spark.jars.repositories", "https://repo1.maven.org/maven2") \
            .config("spark.jars.packages", "org.apache.spark:spark-connect_2.13:3.5.0") \
            .getOrCreate()

    def new_session(self):
        return SparkSession.newSession

    """
    Create DataSet
    """
    def create_frame(self):
        df = spark.createDataFrame([
            Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
            Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
            Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
        ])
        df.show()


    def create_table_temple_view(self, viewName):
        return spark.createOrReplaceTempView(viewName)

    def query(self, query):
        return spark.sql(query)

    def spark_stop(self):
        return self.spark_builder().stop()

    """
    Catalog:
        - Get metadata from the Catalog
        - List databases
        - Output
        [Database(name='default', description='default database', 
        locationUri='file:/Users/admin/.spyder-py3/spark-warehouse')]
    """
    def databases(self):
        return spark.catalog.listDatabases()

    """
    Output
    [Table(name='sample_hive_table', database='default', description=None, tableType='MANAGED', #isTemporary=False), 
    Table(name='sample_hive_table1', database='default', description=None, #tableType='MANAGED', isTemporary=False), 
    Table(name='sample_hive_table121', database='default', #description=None, tableType='MANAGED', isTemporary=False), 
    Table(name='sample_table', database=None, #description=None, tableType='TEMPORARY', isTemporary=True)]
    """
    def tables(self):
        return spark.catalog.listTables()
