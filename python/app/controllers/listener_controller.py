"""HTTP routes for the webhook listener."""

import logging

from fastapi import APIRouter, Header, Request
from fastapi.responses import PlainTextResponse

from app.config import settings
from app.services import listener

log = logging.getLogger("ListenerController")

router = APIRouter(prefix="/api", tags=["webhooks"])


@router.post("/listenevent", response_class=PlainTextResponse)
async def listen_event(
    request: Request,
    x_sumt_signature: str = Header(..., alias="X-SUMT-Signature"),
) -> str:
    """POST /api/listenevent - receives a webhook event from SumTotal."""
    body_bytes = await request.body()
    payload = body_bytes.decode("utf-8")
    secret_key = settings.secret_key

    log.info("Listener Post Method invoked")
    log.info("Payload : %s", payload)
    log.info("secretKey : %s", secret_key)
    log.info("signature : %s", x_sumt_signature)

    return listener.listen_event(x_sumt_signature, payload, secret_key)
