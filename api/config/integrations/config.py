from pydantic import BaseModel

from api.config.integrations.sentry.config import SentryConfig


class IntegrationsConfig(BaseModel):
    sentry: SentryConfig = SentryConfig()

