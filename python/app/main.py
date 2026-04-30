"""FastAPI application entry point - mirrors WebhookListenerJavaApplication."""

import logging

from fastapi import FastAPI

from app.config import settings
from app.controllers.listener_controller import router as listener_router

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)

app = FastAPI(
    title="SumTotal Webhook Listener",
    description="Python sample for receiving and validating SumTotal webhook events.",
    version="0.0.1",
)

app.include_router(listener_router)


@app.get("/")
def root() -> dict:
    return {"status": "ok", "message": "SumTotal Webhook Listener (Python) is running."}
