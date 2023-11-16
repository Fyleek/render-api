import hmac
import json
from typing import Dict

from fastapi import FastAPI, HTTPException, Header, Request
from .services import create_or_update_github_deployment_status
from .utils.secret_token_handler import verify_signature

app = FastAPI()


@app.post("/render-api")
async def router(request: Request, x_hub_signature_256: str = Header(None)):
    payload_body = await request.body()
    try:
        verify = verify_signature(payload_body, x_hub_signature_256)
        if not verify["status"]:
            raise HTTPException(403, detail=verify["message"])
        data = await request.json()
        return create_or_update_github_deployment_status(data)
    except HTTPException as http_e:
        raise HTTPException(http_e.status_code, http_e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error | {e}")
