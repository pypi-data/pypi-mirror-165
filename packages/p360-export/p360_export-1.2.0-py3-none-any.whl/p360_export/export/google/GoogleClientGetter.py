from typing import Dict
from google.ads.googleads.client import GoogleAdsClient

from p360_export.utils.SecretGetterInterface import SecretGetterInterface


class GoogleClientGetter:
    def __init__(
        self,
        secret_getter: SecretGetterInterface,
    ):
        self.__secret_getter = secret_getter

    def get(self, credentials: Dict[str, str]) -> GoogleAdsClient:
        config_dict = {
            "developer_token": self.__secret_getter.get(credentials["developer_token_key"]),
            "refresh_token": self.__secret_getter.get(credentials["refresh_token_key"]),
            "client_id": credentials["client_id"],
            "client_secret": self.__secret_getter.get(credentials["client_secret_key"]),
            "login_customer_id": credentials["customer_id"],
            "use_proto_plus": True,
        }

        return GoogleAdsClient.load_from_dict(config_dict=config_dict)
