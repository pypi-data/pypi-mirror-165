from logging import Logger
from pyspark.sql import SparkSession
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class CheckpointDirSetter(ExportTaskInterface):
    def __init__(self, spark: SparkSession, logger: Logger):
        self.__spark = spark
        self.__logger = logger

    def run(self):
        self.__logger.info("Setting checkpoint dir")

        if not self.__spark.sparkContext.getCheckpointDir():
            self.__spark.sparkContext.setCheckpointDir("dbfs:/tmp/checkpoints")
