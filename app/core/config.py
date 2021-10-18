from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator
from typing import List, Optional, Dict, Any

import os
import json

from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

settings = Settings()
            