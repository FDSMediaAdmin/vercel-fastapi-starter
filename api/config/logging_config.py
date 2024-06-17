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
                "sink": "app.log",
                "rotation": "1 MB",
                "retention": "10 days",
                "level": "INFO",
                "format": "{time} {level} {message}",
            },
        ],
    }
    logger.configure(**config)
