from typing import Optional
from pyspark.sql import DataFrame
from p360_interface_bundle.clickhouse.ClickHouseContext import ClickHouseContext


class ClickHouseTableUploader:
    __engine_map = {
        "summing_merge_tree": "ENGINE = SummingMergeTree() ORDER BY {order_column}",
        "aggregating_merge_tree": "ENGINE = AggregatingMergeTree() ORDER BY {order_column}",
        "log": "ENGINE = Log",
    }

    def __init__(self, clickhouse_context: ClickHouseContext):
        self.__clickhouse_context = clickhouse_context

    def upload(self, df: DataFrame, table_name: str, engine_type: str, order_column: Optional[str] = None):
        if engine_type not in self.__engine_map:
            raise Exception(f"Invalid engine type '{engine_type}', allowed types are {self.__engine_map.keys()}")

        if engine_type in ["summing_merge_tree", "aggregating_merge_tree"] and order_column is None:
            raise Exception(f"You must specify order column for engine type of '{engine_type}'")

        (
            df.write.format("jdbc")
            .option("createTableOptions", self.__engine_map[engine_type].format(order_column=order_column))
            .option("driver", "com.clickhouse.jdbc.ClickHouseDriver")
            .option("url", f"jdbc:clickhouse://{self.__clickhouse_context.get_host()}:{self.__clickhouse_context.get_port()}")
            .option("dbtable", table_name)
            .option("user", self.__clickhouse_context.get_user())
            .option("password", self.__clickhouse_context.get_password())
            .mode("overwrite")
            .save()
        )
