import json
import requests
from p360_interface_bundle.clickhouse.ClickHouseContext import ClickHouseContext


class ClickHouseQueryExecutor:
    def __init__(self, clickhouse_context: ClickHouseContext):
        self.__clickhouse_context = clickhouse_context

    def execute(self, query: str):
        url = f"http://{self.__clickhouse_context.get_host()}:{self.__clickhouse_context.get_port()}/"

        params = {
            "user": self.__clickhouse_context.get_user(),
            "password": self.__clickhouse_context.get_password(),
            "default_format": "JSON",
        }

        response = requests.post(url=url, params=params, data=query)

        if not response.ok:
            raise Exception(f"Error executing clickhouse query '{query}', response {response.content}")

        return json.loads(response.content.decode("utf-8") or "{}").get("data")
