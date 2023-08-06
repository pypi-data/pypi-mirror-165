from logging import Logger
from pyspark.sql import DataFrame
from pyspark.sql import functions as f
from featurestorebundle.entity.EntityGetter import EntityGetter
from featurestorebundle.feature.FeatureStore import FeatureStore
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class FeatureStoreLoader(ExportTaskInterface):
    def __init__(self, feature_store: FeatureStore, entity_getter: EntityGetter, logger: Logger):
        self.__feature_store = feature_store
        self.__entity_getter = entity_getter
        self.__logger = logger

    def run(self):
        self.__logger.info("Loading Feature Store")

        entity = self.__entity_getter.get()

        feature_store = self.__feature_store.get_latest(entity.name, exclude_tags=["private"], skip_incomplete_rows=True)
        feature_store = self.__convert_types(feature_store)
        feature_store = feature_store.checkpoint()

        feature_store.createOrReplaceTempView("feature_store")

        self.__logger.info("Loading Feature Store done")

    def __convert_types(self, feature_store: DataFrame) -> DataFrame:
        converted_features = []

        for col, dtype in feature_store.dtypes:
            if dtype == "double" or "decimal" in dtype:
                converted_features.append(f.col(col).cast("float"))
                continue

            if dtype == "boolean":
                converted_features.append(f.col(col).cast("byte"))
                continue

            converted_features.append(f.col(col))

        return feature_store.select(*converted_features).replace(float("nan"), None)
