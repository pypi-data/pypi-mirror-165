import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv(dotenv_path=".env")


class Configuration(BaseSettings):
    empower_api_url: str = os.environ.get("EMPOWER_API_URL")
    empower_discovery_url: str = os.environ.get("EMPOWER_DISCOVERY_URL")
