from typing import Dict, Any

from abc import ABC, abstractmethod
from pyspark.sql import DataFrame


class DataBuilderInterface(ABC):
    @property
    @abstractmethod
    def data_location(self):
        pass

    @abstractmethod
    def build(self, config: Dict[str, Any]) -> DataFrame:
        pass
