from typing import Dict

from render_api.utils import get_token


def get_headers(app: str) -> Dict[str, str]:
    headers_config = {
        "github": {
            "Authorization": f"Bearer {get_token('github_token')}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        "render": {
            "Accept": "application/json",
            "Authorization": f"Bearer {get_token('render_token')}",
        },
    }
    return headers_config.get(app, {})
