from box import Box
from pyspark.dbutils import DBUtils


class ClickHouseContext:
    def __init__(self, clickhouse_config: Box, dbutils: DBUtils):
        self.__clickhouse_config = clickhouse_config
        self.__dbutils = dbutils

    def get_host(self):
        return self.__clickhouse_config.host

    def get_port(self):
        return self.__clickhouse_config.port

    def get_user(self):
        return self.__dbutils.secrets.get(
            scope=self.__clickhouse_config.credentials.user.secret_scope, key=self.__clickhouse_config.credentials.user.secret_key
        )

    def get_password(self):
        return self.__dbutils.secrets.get(
            scope=self.__clickhouse_config.credentials.password.secret_scope, key=self.__clickhouse_config.credentials.password.secret_key
        )
