from typing import Dict, Any
from p360_export.P360ExportManager import P360ExportManager
from p360_export.data.build.FeatureStoreDataBuilder import FeatureStoreDataBuilder
from p360_export.query.QueryBuilder import QueryBuilder


class P360ExportRunner:
    def __init__(
        self,
        manager: P360ExportManager,
        query_builder: QueryBuilder,
        data_builder: FeatureStoreDataBuilder,
    ):
        self.__manager = manager
        self.__query_builder = query_builder
        self.__data_builder = data_builder

    def export(self, config: Dict[str, Any]):
        query, table_id = self.__query_builder.build(config)

        base_df = self.__data_builder.build(config)

        df = self.__manager.get_data_picker(config).pick(df=base_df, query=query, table_id=table_id, config=config)

        self.__manager.get_exporter(config).export(df, config)
