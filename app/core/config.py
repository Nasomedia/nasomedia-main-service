from pydantic import AnyHttpUrl, BaseSettings
from typing import List

import os
import json

from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

settings = Settings()
