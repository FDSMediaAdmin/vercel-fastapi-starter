from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
import sentry_sdk
from loguru import logger

from .config.config import settings
from .config.logging_config import configure_logging
from .routers.v1 import main as v1_main
from .routers.v2 import main as v2_main


app = FastAPI()

# Configure Loguru logger
configure_logging()
logger.debug('sentry dsn: {}'.format(settings.integrations.sentry.dsn))

if settings.env == 'production' or settings.env == 'development':
    sentry_sdk.init(
        environment=settings.env,
        dsn=settings.integrations.sentry.dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )

app.include_router(v1_main.router)
app.include_router(v2_main.router)


app = VersionedFastAPI(app, enable_latest=True)
