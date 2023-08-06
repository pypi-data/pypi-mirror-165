from typing import Dict, Any

from p360_export.export.sfmc.SFMCData import SFMCData
from p360_export.utils.SecretGetterInterface import SecretGetterInterface


class SFMCDataGetter:
    def __init__(
        self,
        secret_getter: SecretGetterInterface,
    ):
        self.__secret_getter = secret_getter

    def get(self, config: Dict[str, Any]):
        return SFMCData(
            client_secret=self.__secret_getter.get(key=config["credentials"]["client_secret_key"]),
            ftp_password=self.__secret_getter.get(key=config["credentials"]["ftp_password_key"]),
            config=config,
        )
