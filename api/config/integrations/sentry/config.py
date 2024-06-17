from pydantic import BaseModel
# Import the necessary module
from dotenv import load_dotenv
import os

load_dotenv()

class SentryConfig(BaseModel):
    dsn: str = os.getenv("SENTRY_DSN", None)
