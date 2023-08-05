from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import requests

USER_AGENT = "KrakenSpot/Py"


@dataclass
class KrakenResponse:
    result: Dict = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


@dataclass
class HTTPResponse:
    status_code: int
    body: Dict[str, Any]


def http_get(url: str, params: Optional[Dict[str, str]] = None) -> HTTPResponse:
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, params=params)
    return HTTPResponse(
        status_code=r.status_code,
        body=r.json(),
    )


def http_post(
    url: str,
    body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> HTTPResponse:
    if not headers:
        headers = {}
    headers["User-Agent"] = USER_AGENT
    r = requests.post(url, headers=headers, data=body)
    return HTTPResponse(
        status_code=r.status_code,
        body=r.json(),
    )


def clean_params(params: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for key, value in params.items():
        if value == True:
            out[key] = "true"
        elif value == False:
            out[key] = "false"
        elif value != None:
            out[key] = str(value)
    return out
