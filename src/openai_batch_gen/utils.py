import base64
import mmh3
from typing import Union, Callable
import uuid

def _hash64(hash_function: Callable[[bytes], bytes], b: Union[bytes, str]) -> str:
    if isinstance(b, str):
        b = b.encode("utf-8")
    return base64.urlsafe_b64encode(hash_function(b)).decode("utf-8").rstrip("=").replace("_", "-")

def mmh3_64(b: Union[bytes, str]) -> str:
    return _hash64(lambda b: mmh3.mmh3_32_digest(b), b)

def uuid64() -> str:
    return mmh3_64(uuid.uuid4().bytes)
