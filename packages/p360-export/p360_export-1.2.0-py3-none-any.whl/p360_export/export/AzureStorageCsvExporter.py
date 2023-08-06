import os
from typing import Dict, Any

from pyspark.sql import DataFrame, SparkSession
from pyspark.dbutils import DBUtils

from p360_export.export.ExporterInterface import ExporterInterface


class AzureStorageCsvExporter(ExporterInterface):
    def __init__(self, spark: SparkSession):
        self.__spark = spark

    @property
    def export_destination(self):
        return "dataplatform"

    def export(self, df: DataFrame, config: Dict[str, Any]):
        config_id = config.get("id")
        df.toPandas().to_csv("/dbfs/tmp/tmpxol6w4xe.csv")  # pyre-ignore[16]
        dbutils = DBUtils(self.__spark)
        exports_base_path = config["credentials"]["csv_exports_base_path"]
        dbutils.fs.mv("dbfs:/tmp/tmpxol6w4xe.csv", os.path.join(exports_base_path, config_id + ".csv"))
