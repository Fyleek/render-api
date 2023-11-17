import json
import os
import hashlib
import hmac
from typing import Dict, Union

from constants import TOKENS_FILE

_local_tokens = None


def get_token(token_name: str) -> str:
    global _local_tokens

    # Try to get the token from environment variables
    token = os.getenv(token_name.upper())
    if token:
        return token

    # Load tokens from the local file if not already done
    if _local_tokens is None:
        with open(TOKENS_FILE, "r") as file:
            _local_tokens = json.load(file)

    return _local_tokens.get(token_name.upper(), "")


def verify_signature(payload_body, signature_header) -> Dict[str, Union[str, bool]]:
    secret_token = get_token("WEBHOOK_TOKEN")
    if not secret_token:
        return {"message": "Webhook secret token is not available.", "status": False}
    if not signature_header:
        return {"message": "x-hub-signature-256 header is missing!", "status": False}
    hash_object = hmac.new(secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        return {"message": "Request signatures didn't match!", "status": False}
    return {"message": "signatures match!", "status": True}
