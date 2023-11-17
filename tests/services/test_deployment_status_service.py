import pytest
from unittest import mock

from constants import RENDER_ROOT
from render_api.services.deployment_status_service import (
    create_github_deployment_status,
    create_github_deployment,
    get_render_service_id,
    get_render_deployment_status,
    manage_deployment_status,
)

bearer = "Bearer testtoken"
full_name = "user/repo"

@pytest.fixture
def mock_all():
    with mock.patch(
        "render_api.services.deployment_status_service.get_render_service_id"
    ) as mock_get_render_service_id, mock.patch(
        "render_api.services.deployment_status_service.get_render_deployment_status"
    ) as mock_get_render_deployment_status, mock.patch(
        "render_api.services.deployment_status_service.create_github_deployment"
    ) as mock_create_github_deployment, mock.patch(
        "render_api.services.deployment_status_service.create_github_deployment_status"
    ) as mock_create_github_deployment_status, mock.patch(
        "render_api.services.deployment_status_service.logger.error"
    ) as mock_logger_error, mock.patch(
        "time.sleep"
    ) as mock_sleep, mock.patch(
        "render_api.services.deployment_status_service.session.post"
    ) as mock_post, mock.patch(
        "render_api.services.deployment_status_service.session.get"
    ) as mock_get, mock.patch(
        "render_api.services.deployment_status_service.get_headers"
    ) as mock_get_headers:
        mocks = {
            "get_render_service_id": mock_get_render_service_id,
            "get_render_deployment_status": mock_get_render_deployment_status,
            "create_github_deployment": mock_create_github_deployment,
            "create_github_deployment_status": mock_create_github_deployment_status,
            "logger_error": mock_logger_error,
            "sleep": mock_sleep,
            "post": mock_post,
            "get": mock_get,
            "get_headers": mock_get_headers,
        }
        yield mocks


def test_create_github_deployment_status(mock_all):
    mock_all["get_headers"].return_value = {"Authorization": f"{bearer}"}
    mock_response = mock.Mock()
    mock_response.status_code = 201
    mock_all["post"].return_value = mock_response

    create_github_deployment_status(
        "owner", "repo", "status", "render_id", "user_repo", "deployment_id"
    )

    mock_all["get_headers"].assert_called_once_with("github")
    mock_all["post"].assert_called_once()
    args, kwargs = mock_all["post"].call_args
    assert args[0] == "https://api.github.com/repos/user_repo/deployments/deployment_id/statuses"
    assert kwargs["json"] == {
        "owner": "owner",
        "repo": "repo",
        "state": "status",
        "deployment_id": "render_id",
        "environment": "Production",
        "description": "Deployment status from Render",
    }


def test_create_github_deployment(mock_all):
    mock_all["get_headers"].return_value = {"Authorization": f"{bearer}"}
    mock_response = mock.Mock()
    mock_response.json.return_value = {"id": "123456"}
    mock_response.status_code = 201
    mock_all["post"].return_value = mock_response

    deployment_id = create_github_deployment("user_repo", "repo", "owner")

    mock_all["get_headers"].assert_called_once_with("github")
    mock_all["post"].assert_called_once()
    args, kwargs = mock_all["post"].call_args
    assert args[0] == "https://api.github.com/repos/user_repo/deployments"
    assert kwargs["json"] == {
        "owner": "owner",
        "repo": "repo",
        "ref": "main",
        "environment": "Production",
        "production_environment": True,
        "description": "Deployment status from Render",
    }
    assert deployment_id == "123456"


def test_get_render_service_id(mock_all):
    mock_all["get_headers"].return_value = {"Authorization": f"{bearer}"}
    mock_response = mock.Mock()
    mock_response.json.return_value = [{"service": {"repo": "repo", "id": "service_id"}}]
    mock_response.status_code = 200
    mock_all["get"].return_value = mock_response

    service_id = get_render_service_id("repo")

    mock_all["get_headers"].assert_called_once_with("render")
    mock_all["get"].assert_called_once_with(
        f"{RENDER_ROOT}/services", headers={"Authorization": f"{bearer}"}
    )
    assert service_id == "service_id"


def test_get_render_deployment_status(mock_all):
    mock_all["get_headers"].return_value = {"Authorization": f"{bearer}"}
    mock_response = mock.Mock()
    mock_response.json.return_value = [{"deploy": {"status": "success", "id": "deployment_id"}}]
    mock_response.status_code = 200
    mock_all["get"].return_value = mock_response

    service_status = get_render_deployment_status("service_id")

    mock_all["get_headers"].assert_called_once_with("render")
    mock_all["get"].assert_called_once_with(
        f"{RENDER_ROOT}/services/service_id/deploys", headers={"Authorization": f"{bearer}"}
    )
    assert service_status == {"status": "success", "id": "deployment_id"}


def test_manage_deployment_status(mock_all):
    mock_all["get_render_service_id"].return_value = "service_id"
    mock_all["get_render_deployment_status"].return_value = {
        "status": "live",
        "id": "deployment_id",
    }
    mock_all["create_github_deployment"].return_value = "github_deployment_id"

    test_data = {
        "pull_request": {"state": "closed", "merged": True},
        "repository": {
            "full_name": f"{full_name}",
            "html_url": "https://example.com/repo",
            "owner": {"login": "user"},
            "name": "repo",
        },
    }

    manage_deployment_status(test_data)

    mock_all["get_render_service_id"].assert_called_once_with("https://example.com/repo")
    mock_all["get_render_deployment_status"].assert_called_once_with("service_id")
    mock_all["create_github_deployment"].assert_called_once_with(f"{full_name}", "repo", "user")
    mock_all["create_github_deployment_status"].assert_called_once_with(
        "user", "repo", "success", "deployment_id", f"{full_name}", "github_deployment_id"
    )

    mock_all["logger_error"].assert_not_called()
