from logging import Logger
from box import Box
from p360_interface_bundle.clickhouse.ClickHouseTableExistenceChecker import ClickHouseTableExistenceChecker
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class ExportCollisionChecker(ExportTaskInterface):
    def __init__(self, logger: Logger, clickhouse_table_existence_checker: ClickHouseTableExistenceChecker, export_tables: Box):
        self.__clickhouse_table_existence_checker = clickhouse_table_existence_checker
        self.__logger = logger
        self.__export_tables = export_tables

    def run(self):
        self.__logger.info("Checking if another export is in progress")

        if self.__clickhouse_table_existence_checker.exist(self.__export_tables.features_temp):
            raise Exception("Clickhouse export is already ongoing in this environment")

        self.__logger.info("No other export in progress")
