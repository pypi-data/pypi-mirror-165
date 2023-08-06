from p360_interface_bundle.clickhouse.ClickHouseQueryExecutor import ClickHouseQueryExecutor


class ClickHouseTableExistenceChecker:
    def __init__(self, clickhouse_query_executor: ClickHouseQueryExecutor):
        self.__clickhouse_query_executor = clickhouse_query_executor

    def exist(self, table_name: str) -> bool:
        response = self.__clickhouse_query_executor.execute(f"EXISTS {table_name}")

        return response[0]["result"] == 1
