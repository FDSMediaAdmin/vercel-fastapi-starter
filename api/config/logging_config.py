from loguru import logger
import sys

def configure_logging():
    config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "level": "DEBUG",
                "format": "<green>{time}</green> <level>{message}</level>",
            },
            {
                "sink": "logs/app.log",
                "rotation": "1 MB",
                "retention": "10 days",
                "level": "DEBUG",
                "format": "{time:YYYY-MM-DD at HH:mm:ss} {level} {message}",
            },
        ],
    }
    logger.configure(**config)
