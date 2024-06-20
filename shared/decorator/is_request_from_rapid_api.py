from fastapi import Header, HTTPException

from loguru import logger
from typing_extensions import Annotated

from api.config.config import settings


def is_request_from_rapid_api(x_rapidapi_host: Annotated[str, Header()],
                              x_rapidapi_version: Annotated[str, Header()],
                              x_rapidapi_request_id: Annotated[str, Header()],
                              x_rapidapi_user: Annotated[str, Header()],
                              x_rapidapi_subscription: Annotated[str, Header()],
                              x_request_id: Annotated[str, Header()]):
    if settings.integrations.rapidapi.use_rapidapi and settings.integrations.rapidapi.use_rapidapi_checking:
        if not (x_rapidapi_host is not None and \
                x_rapidapi_user is None and \
                x_request_id is None and \
                x_rapidapi_subscription is None and \
                x_rapidapi_version is None and \
                x_rapidapi_request_id):
            return
        else:
            raise HTTPException(status_code=401, detail="Request not from rapidapi")
        return
    else:
        return
