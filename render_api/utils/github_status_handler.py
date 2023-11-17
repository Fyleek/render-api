def get_github_status(render_status: str) -> str:
    #  Link between render and github status
    state_mapping = {
        "build_in_progress": "in_progress",
        "created": "in_progress",
        "update_in_progress": "in_progress",
        "pre_deploy_in_progress": "in_progress",
        "live": "success",
        "build_failed": "failure",
        "update_failed": "failure",
        "pre_deploy_failed": "failure",
        "canceled": "cancel",
        "deactivated": "inactive",
    }

    return state_mapping.get(render_status, "error")
