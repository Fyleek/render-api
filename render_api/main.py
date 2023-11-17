from fastapi import FastAPI, Header, Request

from logging_config import logger
from .services import manage_deployment_status
from .utils.secret_token_handler import verify_signature

app = FastAPI()


@app.post("/render-api")
async def router(request: Request, x_hub_signature_256: str = Header(None)):
    payload_body = await request.body()
    try:
        verify = verify_signature(payload_body, x_hub_signature_256)
        if not verify["status"]:
            logger.error(f"Error 403 {verify['message']}")
        data = await request.json()
        manage_deployment_status(data)
    except Exception as exc:
        logger.error(f"Exception | {exc}")
