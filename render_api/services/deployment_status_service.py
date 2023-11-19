import time
from functools import wraps
from typing import Dict

import requests

from constants import GITHUB_ROOT, RENDER_ROOT
from logging_config import logger
from render_api.utils import get_headers, get_github_status

session = requests.Session()


# Decorator for logging and error handling
def log_and_handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            logger.error(f"Exception in {func.__name__}| {exc}")
            return None

    return wrapper


@log_and_handle_errors
def manage_deployment_status(data: Dict):
    pr = data["pull_request"]
    repo_data = data["repository"]
    state, merged = pr["state"], pr["merged"]
    user_repo, repo_url = repo_data["full_name"], repo_data["html_url"]
    owner, repo = repo_data["owner"]["login"], repo_data["name"]

    if not (merged and state == "closed"):
        return

    service_id = get_render_service_id(repo_url)
    if not service_id:
        logger.error("Render service ID is null")
        return

    deployment_status = get_render_deployment_status(service_id)
    if not deployment_status:
        return

    process_deployment_status(user_repo, repo, owner, deployment_status, service_id)


@log_and_handle_errors
def process_deployment_status(user_repo, repo, owner, deployment_status, service_id):
    github_status = get_github_status(deployment_status["status"])
    deployment_id = deployment_status["id"]
    github_deployment_id = create_github_deployment(user_repo, repo, owner)

    if not github_deployment_id:
        logger.error("Failed to create GitHub deployment")
        return

    update_github_deployment_status(
        owner, repo, github_status, deployment_id, user_repo, github_deployment_id, service_id
    )


@log_and_handle_errors
def update_github_deployment_status(
    owner, repo, status, deployment_id, user_repo, github_deployment_id, service_id
):
    create_github_deployment_status(
        owner, repo, status, deployment_id, user_repo, github_deployment_id
    )
    new_status = ""
    while new_status not in ["failure", "success"]:
        new_render_deployment_status = get_render_deployment_status(service_id)
        new_status = get_github_status(new_render_deployment_status["status"])
        time.sleep(
            10
        )  # You can remove it (but it's better to not spam the render API [400 GET request/minutes])
    create_github_deployment_status(
        owner, repo, new_status, deployment_id, user_repo, github_deployment_id
    )


@log_and_handle_errors
def get_render_deployment_status(service_id: str) -> Dict:
    url = f"{RENDER_ROOT}/services/{service_id}/deploys"
    response = session.get(url, headers=get_headers("render"))
    logger.info(f"GET: {url} executed with status_code: {response.status_code}")
    data = response.json()[0]["deploy"]
    return {"status": data["status"], "id": data["id"]}


@log_and_handle_errors
def get_render_service_id(repo: str) -> str:
    url = f"{RENDER_ROOT}/services"
    response = session.get(url, headers=get_headers("render"))
    logger.info(f"GET: {url} executed with status_code: {response.status_code}")
    for service in response.json():
        if service["service"]["repo"] == repo:
            return service["service"]["id"]


@log_and_handle_errors
def create_github_deployment(user_repo: str, repo: str, owner: str) -> str:
    url = f"{GITHUB_ROOT}/repos/{user_repo}/deployments"
    data = {
        "owner": owner,
        "repo": repo,
        "ref": "main",
        "environment": "Production",
        "production_environment": True,
        "description": "Deployment status from Render",
    }
    response = session.post(url, headers=get_headers("github"), json=data)
    logger.info(f"POST: {url} executed with status_code: {response.status_code}")
    return response.json().get("id")


@log_and_handle_errors
def create_github_deployment_status(
    owner: str,
    repo: str,
    status: str,
    render_deployment_id: str,
    user_repo: str,
    github_deployment_id: str,
):
    url = f"{GITHUB_ROOT}/repos/{user_repo}/deployments/{github_deployment_id}/statuses"
    data = {
        "owner": owner,
        "repo": repo,
        "state": status,
        "deployment_id": render_deployment_id,
        "environment": "Production",
        "description": "Deployment status from Render",
    }
    response = session.post(url, headers=get_headers("github"), json=data)
    logger.info(f"POST: {url} executed with status_code: {response.status_code}")
