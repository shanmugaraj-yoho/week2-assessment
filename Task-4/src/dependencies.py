import os
import secrets

from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("Api key is missing from .env")

def verify_api_key(x_api_key: str = Header(None, alias="X-API-key")): # specofy exact header name

    if x_api_key is None:
        raise HTTPException(status_code=401, detail="No API key")

    if not secrets.compare_digest(x_api_key,API_KEY): # safely compare api key
        raise HTTPException(status_code=403, detail="Invalid API key")

    return True