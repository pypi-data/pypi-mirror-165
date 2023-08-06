from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class SFMCData:  # pylint: disable=R0902
    client_secret: str
    ftp_password: str
    config: Dict[str, Any]

    @property
    def client_id(self) -> str:
        return self.config["credentials"]["client_id"]

    @property
    def tenant_url(self) -> str:
        return self.config["credentials"]["tenant_url"]

    @property
    def account_id(self) -> str:
        return self.config["credentials"]["account_id"]

    @property
    def file_location(self) -> str:
        return self.config["credentials"]["file_location"]

    @property
    def ftp_username(self) -> str:
        return self.config["credentials"]["ftp_username"]

    @property
    def export_columns(self) -> List[str]:
        return self.config["params"]["export_columns"]

    @property
    def subscriber_key(self) -> str:
        return self.config["params"]["mapping"]["subscriber_key"]

    @property
    def audience_name(self) -> str:
        return f"p360-{self.config['export_title']}"

    @property
    def new_field_names(self) -> List[str]:
        return self.export_columns + [self.subscriber_key]
