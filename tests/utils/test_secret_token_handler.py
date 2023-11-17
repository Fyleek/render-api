import json
import os
import hmac
import hashlib
from unittest.mock import patch, mock_open

from render_api.utils.secret_token_handler import get_token, verify_signature

# Test data
payload_body = b"test payload"
secret_token = "test_secret"
signature_header = (
    "sha256="
    + hmac.new(secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256).hexdigest()
)


# Test when token is available as an environment variable
@patch.dict(os.environ, {"GITHUB_TOKEN": "test_github_token"})
def test_get_token_from_env():
    assert get_token("github_token") == "test_github_token"


# Test when token is not in env but in a local file
@patch.dict(os.environ, {}, clear=True)
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data=json.dumps({"GITHUB_TOKEN": "local_github_token"}),
)
def test_get_token_from_file(mock_file):
    assert get_token("github_token") == "local_github_token"


# Test when token is neither in env nor in the local file
@patch.dict(os.environ, {}, clear=True)
@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({}))
def test_get_token_not_found(mock_file):
    assert get_token("") == ""


# Test when the secret token is not available
@patch("render_api.utils.secret_token_handler.get_token", return_value=None)
def test_verify_signature_no_secret_token(mock_get_token):
    result = verify_signature(payload_body, signature_header)
    assert result == {"message": "Webhook secret token is not available.", "status": False}


# Test when the signature header is missing
@patch("render_api.utils.secret_token_handler.get_token", return_value=secret_token)
def test_verify_signature_no_signature_header(mock_get_token):
    result = verify_signature(payload_body, None)
    assert result == {"message": "x-hub-signature-256 header is missing!", "status": False}


# Test for a successful signature match
@patch("render_api.utils.secret_token_handler.get_token", return_value=secret_token)
def test_verify_signature_success(mock_get_token):
    result = verify_signature(payload_body, signature_header)
    assert result == {"message": "signatures match!", "status": True}


# Test for a failed signature match
@patch("render_api.utils.secret_token_handler.get_token", return_value=secret_token)
def test_verify_signature_failure(mock_get_token):
    invalid_signature_header = "sha256=invalidsignature"
    result = verify_signature(payload_body, invalid_signature_header)
    assert result == {"message": "Request signatures didn't match!", "status": False}
