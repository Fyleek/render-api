from unittest.mock import patch

from render_api.utils.headers_handler import get_headers

# Test data
github_token = "github_test_token"
render_token = "render_test_token"


# Test for GitHub
@patch("render_api.utils.headers_handler.get_token", return_value=github_token)
def test_get_headers_github(mock_get_token):
    expected_headers = {
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    assert get_headers("github") == expected_headers


# Test for Render
@patch("render_api.utils.headers_handler.get_token", return_value=render_token)
def test_get_headers_render(mock_get_token):
    expected_headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {render_token}",
    }
    assert get_headers("render") == expected_headers


# Test for unknown app
@patch("render_api.utils.headers_handler.get_token", return_value="unknown")
def test_get_headers_unknown_app(mock_get_token):
    assert get_headers("unknown_app") == {}
