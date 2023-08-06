from typing import Dict, Any
from abc import ABC, abstractmethod
from pyspark.sql import DataFrame


class ExporterInterface(ABC):
    @property
    @abstractmethod
    def export_destination(self):
        pass

    @abstractmethod
    def export(self, df: DataFrame, config: Dict[str, Any]):
        pass
