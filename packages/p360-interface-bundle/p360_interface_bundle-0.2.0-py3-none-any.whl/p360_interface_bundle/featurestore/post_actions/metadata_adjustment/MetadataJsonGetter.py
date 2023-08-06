from box import Box
import itertools
from typing import List
from pyspark.sql import types as t, functions as f
from pyspark.sql import DataFrame
from featurestorebundle.feature.FeatureStore import FeatureStore
from featurestorebundle.entity.EntityGetter import EntityGetter

from p360_interface_bundle.featurestore.post_actions.metadata_adjustment.MetadataDatetimeToStringConverter import (
    MetadataDatetimeToStringConverter,
)
from p360_interface_bundle.featurestore.post_actions.metadata_adjustment.StatisticsComputer import StatisticsComputer


class MetadataJsonGetter:
    def __init__(
        self,
        metadata_datetime_to_string_converter: MetadataDatetimeToStringConverter,
        statistics_computer: StatisticsComputer,
        feature_store: FeatureStore,
        entity_getter: EntityGetter,
        general_mapping: Box,
        category_mapping: Box,
    ) -> None:
        self.__metadata_datetime_to_string_converter = metadata_datetime_to_string_converter
        self.__statistics_computer = statistics_computer
        self.__feature_store = feature_store
        self.__entity_getter = entity_getter

        if category_mapping:
            self.__category_mapping = dict(
                itertools.chain(
                    *[list(itertools.product(value, [key])) for key, value in zip(category_mapping.keys(), category_mapping.values())]
                )
            )
        else:
            self.__category_mapping = {}
        self.__general_mapping = general_mapping.to_dict() if general_mapping else {}

    def __get_metadata_with_subcategory(self):
        entity = self.__entity_getter.get()
        metadata = self.__feature_store.get_metadata(entity_name=entity.name)

        return (
            metadata.filter(f.col("entity") == entity.name)
            .withColumn("subcategory", f.col("category"))
            .replace(to_replace=self.__category_mapping, subset=["category"])
        )

    def __add_additional_metadata(self, metadata: DataFrame):
        return metadata.withColumn("type", f.col("variable_type")).withColumn("is_feature", ~f.array_contains("tags", "private"))

    def __rename_metadata(self, df: DataFrame, row: t.Row, general_mapping_dict: dict) -> dict:
        result = {
            (general_mapping_dict[col] if col in general_mapping_dict else col): (row[col] if row[col] is not None else "")
            for col in df.columns
        }
        result["description"] = ""

        return result

    def get_jsons(self) -> List[dict]:
        metadata = self.__get_metadata_with_subcategory()
        metadata = self.__add_additional_metadata(metadata)
        statistics = self.__statistics_computer.compute()

        metadata_rows = metadata.collect()
        category_list = [row.category for row in (metadata.select("category").distinct().collect())]
        all_categories = []
        for category in category_list:
            category_dict = {
                "title": category,
                "category": category,
                "subcategory": "",
                "author": "PX",
            }

            items = []
            for row in metadata_rows:
                if row["category"] == category:
                    item = self.__rename_metadata(metadata, row, self.__general_mapping)
                    item["statistics"] = statistics.get(row.feature)
                    items.append(item)
                    category_dict["items"] = items

            category_dict = self.__metadata_datetime_to_string_converter.convert(category_dict)
            all_categories.append(category_dict)

        return all_categories
