from pyspark.sql import SparkSession


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SparkConfig():
    __metaclass__ = Singleton

    def spark_builder(self):
        return SparkSession.builder.getOrCreate()

    def spark_stop(self):
        return self.spark_builder().stop()
