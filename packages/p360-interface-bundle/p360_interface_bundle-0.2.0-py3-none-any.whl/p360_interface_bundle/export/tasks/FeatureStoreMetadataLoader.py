from logging import Logger
from featurestorebundle.entity.EntityGetter import EntityGetter
from featurestorebundle.feature.FeatureStore import FeatureStore
from p360_interface_bundle.export.ExportTaskInterface import ExportTaskInterface


class FeatureStoreMetadataLoader(ExportTaskInterface):
    def __init__(self, feature_store: FeatureStore, entity_getter: EntityGetter, logger: Logger):
        self.__feature_store = feature_store
        self.__entity_getter = entity_getter
        self.__logger = logger

    def run(self):
        self.__logger.info("Loading Feature Store metadata")

        entity = self.__entity_getter.get()

        feature_store_metadata = self.__feature_store.get_metadata(entity.name, exclude_tags=["private"])

        feature_store_metadata.createOrReplaceTempView("feature_store_metadata")

        self.__logger.info("Loading Feature Store metadata done")
