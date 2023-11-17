import pytest
from render_api.utils.github_status_handler import get_github_status


# Mapping des statuts Render aux statuts GitHub
@pytest.mark.parametrize("render_status, expected_github_status", [
    ("build_in_progress", "in_progress"),
    ("created", "in_progress"),
    ("update_in_progress", "in_progress"),
    ("pre_deploy_in_progress", "in_progress"),
    ("live", "success"),
    ("build_failed", "failure"),
    ("update_failed", "failure"),
    ("pre_deploy_failed", "failure"),
    ("canceled", "cancel"),
    ("deactivated", "inactive"),
    ("non_existent_status", "error")
])
def test_get_github_status(render_status, expected_github_status):
    assert get_github_status(render_status) == expected_github_status
