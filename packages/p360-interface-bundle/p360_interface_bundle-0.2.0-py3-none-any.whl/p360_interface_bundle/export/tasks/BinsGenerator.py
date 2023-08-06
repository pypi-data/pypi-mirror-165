from logging import Logger
from box import Box
from pyspark.sql import SparkSession
from p360_interface_bundle.export.bins.IntegralBinsGenerator import IntegralBinsGenerator
from p360_interface_bundle.export.bins.FloatingPointBinsGenerator import FloatingPointBinsGenerator
from p360_interface_bundle.export.bins.CategoricalBinsReducer import CategoricalBinsReducer
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class BinsGenerator(ExportTaskInterface):
    def __init__(
        self,
        spark: SparkSession,
        logger: Logger,
        integral_bins_generator: IntegralBinsGenerator,
        floating_point_bins_generator: FloatingPointBinsGenerator,
        categorical_bins_reducer: CategoricalBinsReducer,
        bin_params: Box,
    ):
        self.__spark = spark
        self.__logger = logger
        self.__integral_bins_generator = integral_bins_generator
        self.__floating_point_bins_generator = floating_point_bins_generator
        self.__categorical_bins_reducer = categorical_bins_reducer
        self.__bin_params = bin_params

    def run(self):
        self.__logger.info("Generating bins")

        feature_store = self.__spark.read.table("feature_store")
        sampled_feature_store = self.__spark.read.table("sampled_feature_store")
        feature_store_metadata = self.__spark.read.table("feature_store_metadata")

        integral_bins = self.__integral_bins_generator.generate(feature_store, self.__bin_params.numerical)
        floating_point_bins = self.__floating_point_bins_generator.generate(feature_store, self.__bin_params.numerical)
        numerical_bins = integral_bins.join(floating_point_bins, how="outer")

        categorical_features = [row.feature for row in feature_store_metadata.collect() if row.variable_type == "categorical"]
        reduced_categorical_bins = self.__categorical_bins_reducer.reduce(
            sampled_feature_store, categorical_features, self.__bin_params.categorical
        )

        numerical_bins.checkpoint().createOrReplaceTempView("bins")
        reduced_categorical_bins.checkpoint().createOrReplaceTempView("reduced_sampled_feature_store")

        self.__logger.info("Generating bins done")
