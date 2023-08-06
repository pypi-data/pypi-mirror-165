from pyspark.sql import DataFrame
from featurestorebundle.entity.getter import get_entity
from featurestorebundle.feature.FeatureStore import FeatureStore
from typing import List, Set, Dict, Any

from p360_export.data.build.DataBuilderInterface import DataBuilderInterface


class FeatureStoreDataBuilder(DataBuilderInterface):
    def __init__(self, feature_store: FeatureStore) -> None:
        self.__feature_store = feature_store

    @property
    def data_location(self):
        return "feature_store"

    def build(self, config: Dict[str, Any]) -> DataFrame:
        entity = get_entity()
        attributes = self._get_required_attribute_names(config=config)

        return self.__feature_store.get_latest(entity.name, features=attributes)

    def _get_required_attribute_names(self, config: Dict[str, Any]) -> List[str]:
        attributes_from_export_columns = set(config.get("params", {}).get("export_columns", []))
        attributes_from_mapping = set(config.get("params", {}).get("mapping", {}).values())
        segments = config.get("segments", [])
        attributes_from_condition = self._get_attributes_from_segments(segments)

        return list(attributes_from_export_columns | attributes_from_mapping | attributes_from_condition)

    def _get_attributes_from_segments(self, segments: List[dict]) -> Set[str]:
        attributes = set()
        for segment in segments:
            attributes.update(self._get_attributes_from_definition_segment(segment["definition_segment"]))

        return attributes

    def _get_attributes_from_definition_segment(self, definition_segment: List[dict]) -> Set[str]:
        attributes = set()
        for definition_part in definition_segment:
            attributes.update(self._get_attribute_ids(definition_part["attributes"]))

        return attributes

    def _get_attribute_ids(self, attributes: List[dict]) -> Set[str]:
        return {attribute["id"] for attribute in attributes}
