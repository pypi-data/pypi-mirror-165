from logging import Logger
from pyspark.sql import SparkSession
from pyspark.dbutils import DBUtils
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class CheckpointDirCleaner(ExportTaskInterface):
    def __init__(self, spark: SparkSession, dbutils: DBUtils, logger: Logger):
        self.__spark = spark
        self.__dbutils = dbutils
        self.__logger = logger

    def run(self):
        self.__logger.info("Cleaning checkpoint dir")

        if self.__spark.sparkContext.getCheckpointDir():
            self.__dbutils.fs.rm(self.__spark.sparkContext.getCheckpointDir(), recurse=True)
