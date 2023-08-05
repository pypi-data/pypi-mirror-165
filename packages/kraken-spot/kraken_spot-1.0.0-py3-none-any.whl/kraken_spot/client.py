import os
from dataclasses import dataclass
from typing import Optional

from .private import PrivateEndpoints
from .public import PublicEndpoints


@dataclass
class Client(PublicEndpoints, PrivateEndpoints):
    api_key: Optional[str] = None
    private_key: Optional[str] = None
    endpoint: Optional[str] = "https://api.kraken.com"
    api_version: Optional[int] = 0

    def _base_url(self) -> str:
        return f"{self.endpoint}/{self.api_version}"


class DefaultClient(Client):
    """
    The default client will attempt to configure the Kraken client using api keys from
    environment variables. KRAKEN_API_KEY | KRAKEN_PRIVATE_KEY. Both must be set in order
    for them to be used to create a new client.
    """

    def __init__(
        self, endpoint: Optional[str] = None, api_version: Optional[int] = None
    ):
        kwargs = {}
        if endpoint:
            kwargs["endpoint"] = endpoint

        if api_version:
            kwargs["api_version"] = api_version

        if "KRAKEN_API_KEY" in os.environ and "KRAKEN_PRIVATE_KEY" in os.environ:
            kwargs["api_key"] = os.environ["KRAKEN_API_KEY"]
            kwargs["private_key"] = os.environ["KRAKEN_PRIVATE_KEY"]

        return super().__init__(**kwargs)
