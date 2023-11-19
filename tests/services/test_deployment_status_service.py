import pytest
from unittest import mock

from constants import RENDER_ROOT
from render_api.services.deployment_status_service import (
    create_github_deployment_status,
    create_github_deployment,
    get_render_service_id,
    get_render_deployment_status,
    manage_deployment_status,
    process_deployment_status,
    update_github_deployment_status,
    log_and_handle_errors,
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
    ) as mock_get_headers, mock.patch(
        "render_api.services.deployment_status_service.update_github_deployment_status"
    ) as mock_update_github_deployment_status, mock.patch(
        "render_api.services.deployment_status_service.process_deployment_status"
    ) as mock_process_deployment_status, mock.patch(
        "render_api.services.deployment_status_service.manage_deployment_status"
    ) as mock_manage_deployment_status, mock.patch(
        "render_api.services.deployment_status_service.get_github_status"
    ) as mock_get_github_status, mock.patch(
        "render_api.services.deployment_status_service.log_and_handle_errors"
    ) as mock_log_and_handle_errors:
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
            "update_github_deployment_status": mock_update_github_deployment_status,
            "process_deployment_status": mock_process_deployment_status,
            "manage_deployment_status": mock_manage_deployment_status,
            "get_github_status": mock_get_github_status,
            "log_and_handle_errors": mock_log_and_handle_errors,
        }
        yield mocks


@pytest.mark.usefixtures("mock_all")
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


@pytest.mark.usefixtures("mock_all")
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


@pytest.mark.usefixtures("mock_all")
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


@pytest.mark.usefixtures("mock_all")
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


@pytest.mark.usefixtures("mock_all")
def test_update_github_deployment_status(mock_all):
    mock_all["get_render_deployment_status"].side_effect = [
        {"status": "in_progress"},
        {"status": "in_progress"},
        {"status": "success"},
    ]
    mock_all["get_github_status"].side_effect = ["in_progress", "in_progress", "success"]

    update_github_deployment_status(
        "owner",
        "repo",
        "in_progress",
        "deployment_id",
        "user_repo",
        "github_deployment_id",
        "service_id",
    )

    assert mock_all["create_github_deployment_status"].call_count == 2
    initial_call_args = mock_all["create_github_deployment_status"].call_args_list[0]
    final_call_args = mock_all["create_github_deployment_status"].call_args_list[1]

    assert initial_call_args == mock.call(
        "owner", "repo", "in_progress", "deployment_id", "user_repo", "github_deployment_id"
    )
    assert final_call_args == mock.call(
        "owner", "repo", "success", "deployment_id", "user_repo", "github_deployment_id"
    )

    assert mock_all["get_render_deployment_status"].call_count == 3
    assert mock_all["get_github_status"].call_count == 3


@pytest.mark.usefixtures("mock_all")
def test_process_deployment_status(mock_all):
    deployment_status = {"status": "in_progress", "id": "deployment_id"}
    mock_all["get_github_status"].return_value = "in_progress"
    mock_all["create_github_deployment"].return_value = "github_deployment_id"

    process_deployment_status("user_repo", "repo", "owner", deployment_status, "service_id")

    mock_all["get_github_status"].assert_called_once_with("in_progress")
    mock_all["create_github_deployment"].assert_called_once_with("user_repo", "repo", "owner")
    mock_all["update_github_deployment_status"].assert_called_once_with(
        "owner",
        "repo",
        "in_progress",
        "deployment_id",
        "user_repo",
        "github_deployment_id",
        "service_id",
    )

    mock_all["logger_error"].assert_not_called()


@pytest.mark.usefixtures("mock_all")
def test_manage_deployment_status(mock_all):
    test_data = {
        "pull_request": {"state": "closed", "merged": True},
        "repository": {
            "full_name": "user/repo",
            "html_url": "https://example.com/repo",
            "owner": {"login": "user"},
            "name": "repo",
        },
    }

    mock_all["get_render_service_id"].return_value = "service_id"
    mock_all["get_render_deployment_status"].return_value = {
        "status": "live",
        "id": "deployment_id",
    }

    manage_deployment_status(test_data)

    mock_all["get_render_service_id"].assert_called_once_with("https://example.com/repo")
    mock_all["get_render_deployment_status"].assert_called_once_with("service_id")
    mock_all["process_deployment_status"].assert_called_once_with(
        "user/repo", "repo", "user", {"status": "live", "id": "deployment_id"}, "service_id"
    )

    mock_all["logger_error"].assert_not_called()


def test_manage_deployment_status_service_id_null(mock_all):
    mock_all["get_render_service_id"].return_value = None

    test_data = {
        "pull_request": {"state": "closed", "merged": True},
        "repository": {
            "full_name": "user/repo",
            "html_url": "https://example.com/repo",
            "owner": {"login": "user"},
            "name": "repo",
        },
    }

    manage_deployment_status(test_data)

    mock_all["logger_error"].assert_called_once_with("Render service ID is null")

    mock_all["get_render_deployment_status"].assert_not_called()
    mock_all["process_deployment_status"].assert_not_called()


def test_manage_deployment_status_not_merged_or_not_closed(mock_all):
    test_data = {
        "pull_request": {"state": "open", "merged": False},
        "repository": {
            "full_name": "user/repo",
            "html_url": "https://example.com/repo",
            "owner": {"login": "user"},
            "name": "repo",
        },
    }

    manage_deployment_status(test_data)

    mock_all["get_render_service_id"].assert_not_called()
    mock_all["get_render_deployment_status"].assert_not_called()
    mock_all["process_deployment_status"].assert_not_called()
    mock_all["logger_error"].assert_not_called()


def test_manage_deployment_status_no_deployment_status(mock_all):
    test_data = {
        "pull_request": {"state": "closed", "merged": True},
        "repository": {
            "full_name": "user/repo",
            "html_url": "https://example.com/repo",
            "owner": {"login": "user"},
            "name": "repo",
        },
    }

    mock_all["get_render_service_id"].return_value = "service_id"
    mock_all["get_render_deployment_status"].return_value = None

    manage_deployment_status(test_data)

    mock_all["get_render_service_id"].assert_called_once_with("https://example.com/repo")
    mock_all["get_render_deployment_status"].assert_called_once_with("service_id")
    mock_all["process_deployment_status"].assert_not_called()
    mock_all["logger_error"].assert_not_called()


def test_process_deployment_status_no_github_deployment_id(mock_all):
    user_repo = "user/repo"
    repo = "repo"
    owner = "user"
    deployment_status = {"status": "live", "id": "deployment_id"}
    service_id = "service_id"

    mock_all["create_github_deployment"].return_value = None

    process_deployment_status(user_repo, repo, owner, deployment_status, service_id)

    mock_all["create_github_deployment"].assert_called_once_with(user_repo, repo, owner)
    mock_all["update_github_deployment_status"].assert_not_called()
    mock_all["logger_error"].assert_called_once_with("Failed to create GitHub deployment")


def test_log_and_handle_errors_success(mock_all):
    @log_and_handle_errors
    def test_func():
        return "success"

    result = test_func()

    assert result == "success"
    mock_all["logger_error"].assert_not_called()


def test_log_and_handle_errors_exception(mock_all):
    @log_and_handle_errors
    def test_func():
        raise ValueError("Test exception")

    result = test_func()

    assert result is None
    mock_all["logger_error"].assert_called_once_with("Exception in test_func| Test exception")
