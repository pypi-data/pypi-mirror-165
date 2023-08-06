from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "empowercli"
    VERSION: str = "0.1.0"
