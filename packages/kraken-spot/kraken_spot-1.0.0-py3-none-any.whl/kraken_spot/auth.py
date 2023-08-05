import base64
import hashlib
import hmac
import time
import urllib.parse
from typing import Any, Dict

from .errors import AuthError


def generate_nonce() -> int:
    """
    Each API request needs a nonce value that increases on each request. For simplicity
    this will return the current unix timestamp in nanoseconds
    """
    return time.time_ns()


def get_kraken_signature(url_path: str, data: Dict[str, Any], secret: str) -> str:
    """
    Generates a signature for the request. This value will be used in the API-Sign header.
    """
    if "nonce" not in data:
        raise AuthError("missing 'nonce' value when generating signature")

    post_data = urllib.parse.urlencode(data)
    encoded = (str(data["nonce"]) + post_data).encode()
    message = url_path.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sig_digest = base64.b64encode(mac.digest())
    return sig_digest.decode()
