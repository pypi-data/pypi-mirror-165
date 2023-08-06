from logging import Logger
from pyspark.sql import SparkSession
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class SampledFeatureStoreLoader(ExportTaskInterface):
    def __init__(self, spark: SparkSession, logger: Logger, sampling_rate: int):
        self.__spark = spark
        self.__logger = logger
        self.__sampling_rate = sampling_rate

    def run(self):
        self.__logger.info("Loading sampled Feature Store")

        feature_store = self.__spark.read.table("feature_store")

        sampled_feature_store = feature_store.sample(self.__sampling_rate).checkpoint()

        sampled_feature_store.createOrReplaceTempView("sampled_feature_store")

        self.__logger.info("Loading sampled Feature Store done")
