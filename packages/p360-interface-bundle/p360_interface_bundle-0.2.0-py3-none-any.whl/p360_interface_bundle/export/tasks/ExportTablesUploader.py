from logging import Logger
from box import Box
from pyspark.sql import SparkSession
from featurestorebundle.entity.EntityGetter import EntityGetter
from p360_interface_bundle.clickhouse.ClickHouseTableUploader import ClickHouseTableUploader
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class ExportTablesUploader(ExportTaskInterface):
    def __init__(
        self,
        spark: SparkSession,
        logger: Logger,
        entity_getter: EntityGetter,
        clickhouse_table_uploader: ClickHouseTableUploader,
        export_tables: Box,
    ):
        self.__spark = spark
        self.__logger = logger
        self.__entity_getter = entity_getter
        self.__clickhouse_table_uploader = clickhouse_table_uploader
        self.__export_tables = export_tables

    def run(self):
        self.__logger.info("Uploading tables to Clickhouse")

        entity = self.__entity_getter.get()
        feature_store = self.__spark.read.table("feature_store")
        sampled_feature_store = self.__spark.read.table("reduced_sampled_feature_store")
        bins = self.__spark.read.table("bins")

        self.__clickhouse_table_uploader.upload(
            df=feature_store,
            table_name=self.__export_tables.features_temp,
            engine_type="aggregating_merge_tree",
            order_column=entity.id_column,
        )

        self.__clickhouse_table_uploader.upload(
            df=sampled_feature_store,
            table_name=self.__export_tables.sampled_temp,
            engine_type="aggregating_merge_tree",
            order_column=entity.id_column,
        )

        self.__clickhouse_table_uploader.upload(
            df=bins,
            table_name=self.__export_tables.bins_temp,
            engine_type="log",
        )

        self.__logger.info("Uploading tables to Clickhouse done")
