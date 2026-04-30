"""Application configuration loaded from environment / .env file."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    secret_key: str = os.getenv("APPLICATION_SECRET_KEY", "")
    host: str = os.getenv("APPLICATION_HOST", "0.0.0.0")
    port: int = int(os.getenv("APPLICATION_PORT", "8080"))
    log_level: str = os.getenv("APPLICATION_LOG_LEVEL", "INFO")


settings = Settings()
