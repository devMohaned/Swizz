from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Automatically find and load the .env file regardless of where uvicorn is run
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Settings(BaseSettings):
    # Application metadata
    app_name: str = "OPA Policy Evaluation Service"
    opa_url: str
    environment: str = "dev"

    # Integration
    timeout: float = 5.0
    # Logging
    log_format: str = "JSON"
    log_level: str = "INFO"
    log_file_path: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
