# Import the necessary module
from dotenv import load_dotenv
import os

from api.config.db.config import DatabaseConfig

load_dotenv()
# Load environment variables from the .env file (if present)
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings

from api.config.integrations.config import IntegrationsConfig



class Config(BaseSettings):
    integrations: IntegrationsConfig = Field(IntegrationsConfig())
    database: DatabaseConfig = Field(DatabaseConfig())
    env: str = Field(os.getenv("PYTHON_ENV", 'local'))
    API_V1_PREFIX: str = Field('http://localhost:8000/v1_0')


@lru_cache
def get_config() -> Config:
    """get config"""
    return Config()


settings = get_config()
