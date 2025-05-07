from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from ..core import get_app_settings

header_scheme = APIKeyHeader(name="x-api-key")

api_keys:list[str] = get_app_settings().API_KEYS

def check_api_key(api_key: Annotated[str, Depends(header_scheme)]) -> bool:
    if api_key not in api_keys:
        raise HTTPException(status_code=401, detail="invalid api key!")
    return True