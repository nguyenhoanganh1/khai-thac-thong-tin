from OrientDB.configs.spark_config import SparkConfig


class TFIDFService():

    def createConfig(self):
        spark = SparkConfig().spark_builder()
