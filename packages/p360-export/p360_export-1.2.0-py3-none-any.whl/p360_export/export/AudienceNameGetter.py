from typing import Dict, Any


class AudienceNameGetter:
    def get(self, config: Dict[str, Any]) -> str:
        return f"p360-{config['export_title']}"
