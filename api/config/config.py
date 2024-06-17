# Import the necessary module
from dotenv import load_dotenv
import os

load_dotenv()
# Load environment variables from the .env file (if present)
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings

from api.config.integrations.config import IntegrationsConfig



class Config(BaseSettings):
    integrations: IntegrationsConfig = Field(IntegrationsConfig())
    env: str = Field(os.getenv("PYTHON_ENV", 'local'))


@lru_cache
def get_config() -> Config:
    """get config"""
    return Config()


settings = get_config()
