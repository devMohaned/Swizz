from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Automatically find and load the .env file regardless of where uvicorn is run
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_host: str
    database_port: int = 5432
    database_name: str

    # Application metadata
    app_name: str = "User API"
    environment: str = "dev"  # dev, test, preprod, or prod

    # Integration
    opa_service_url: str
    timeout: float = 5.0

    # Authentication
    jwt_secret: str
    jwt_algorithm: str
    jwt_audience: str
    jwt_issuer: str

    # Logging
    log_format: str = "JSON"
    log_level: str = "INFO"
    log_file_path: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
