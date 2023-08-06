from logging import Logger
from box import Box
from p360_interface_bundle.clickhouse.ClickHouseQueryExecutor import ClickHouseQueryExecutor
from p360_interface_bundle.clickhouse.ClickHouseTableExistenceChecker import ClickHouseTableExistenceChecker
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class ExportCommitter(ExportTaskInterface):
    def __init__(
        self,
        export_tables: Box,
        logger: Logger,
        clickhouse_query_executor: ClickHouseQueryExecutor,
        clickhouse_table_existence_checker: ClickHouseTableExistenceChecker,
    ):
        self.__export_tables = export_tables
        self.__logger = logger
        self.__clickhouse_query_executor = clickhouse_query_executor
        self.__clickhouse_table_existence_checker = clickhouse_table_existence_checker

    def run(self):
        self.__commit_table(self.__export_tables.features_main, self.__export_tables.features_temp, self.__export_tables.features_backup)
        self.__commit_table(self.__export_tables.sampled_main, self.__export_tables.sampled_temp, self.__export_tables.sampled_backup)
        self.__commit_table(self.__export_tables.bins_main, self.__export_tables.bins_temp, self.__export_tables.bins_backup)

    def __commit_table(self, main_table: str, temp_table: str, backup_table: str):
        if self.__clickhouse_table_existence_checker.exist(backup_table):
            self.__clickhouse_query_executor.execute(f"DROP TABLE {backup_table}")

        if self.__clickhouse_table_existence_checker.exist(main_table):
            self.__clickhouse_query_executor.execute(f"RENAME TABLE {main_table} TO {backup_table}")

        self.__clickhouse_query_executor.execute(f"RENAME TABLE {temp_table} TO {main_table}")

        self.__logger.info(f"Commit of table '{main_table}' successful, backup saved as {backup_table}")
