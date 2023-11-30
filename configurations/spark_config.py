# from pyspark.shell import spark
# from pyspark.sql import SparkSession
#
#
# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]
#
#
# class SparkConfig:
#     __metaclass__ = Singleton
#
#     # The command we used above to launch the server configured Spark to run as localhost:15002.
#     # So now we can create a remote Spark session on the client using the following command.
#     def getOrCreate(self):
#         return SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
#
#     # Now that the Spark server is running, we can connect to it remotely using Spark Connect.
#     # We do this by creating a remote Spark session on the client where our application runs.
#     # Before we can do that, we need to make sure to stop the existing regular Spark session
#     # because it cannot coexist with the remote Spark Connect session we are about to create.
#     def getOrCreateAfterSessionStop(self):
#         return SparkSession.builder.master("local[*]").getOrCreate().stop()
#
#     def createDataFrame(self, rows):
#         df = spark.createDataFrame(self, rows)
#         return df.show()
