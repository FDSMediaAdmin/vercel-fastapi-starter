from pydantic import BaseModel

from api.config.integrations.sentry.config import SentryConfig
from api.config.integrations.rapidapi.config import RapidApiConfig

class IntegrationsConfig(BaseModel):
    sentry: SentryConfig = SentryConfig()
    rapidapi: RapidApiConfig = RapidApiConfig()
