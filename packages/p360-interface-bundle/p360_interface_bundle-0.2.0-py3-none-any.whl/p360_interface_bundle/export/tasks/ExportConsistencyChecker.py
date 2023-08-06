from logging import Logger
from box import Box
from pyspark.sql import SparkSession
from p360_interface_bundle.clickhouse.ClickHouseQueryExecutor import ClickHouseQueryExecutor
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class ExportConsistencyChecker(ExportTaskInterface):
    def __init__(
        self,
        spark: SparkSession,
        logger: Logger,
        export_tables: Box,
        clickhouse_query_executor: ClickHouseQueryExecutor,
    ):
        self.__spark = spark
        self.__logger = logger
        self.__export_tables = export_tables
        self.__clickhouse_query_executor = clickhouse_query_executor

    def run(self):
        featurestore_count = self.__spark.read.table("feature_store").count()
        clickhouse_count = int(
            self.__clickhouse_query_executor.execute(f"SELECT COUNT(*) from {self.__export_tables.features_main}")[0]["count()"]
        )

        if featurestore_count == clickhouse_count:
            self.__logger.info(f"Export OK: Featurestore row count equals to Clickhouse export row count ({featurestore_count})")

        else:
            raise Exception(
                f"Featurestore row count is not equal to export row count. "
                f"Featurestore: {featurestore_count} | Clickhouse: {clickhouse_count}"
            )
