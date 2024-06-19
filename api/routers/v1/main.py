from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi_versioning import version

from loguru import logger
from typing_extensions import Annotated

from shared.decorator.rapidapi.header_checker import header_check

from api.config.config import settings

router = APIRouter(prefix='/main')
# 'Content-Type'
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

@router.post("/create")
@version(1, 0)
async def main_create():
    logger.debug('main create called')

    return {"message": "main_create: Message sent"}


@router.get("/read", dependencies=[Depends(is_request_from_rapid_api)])
@version(1, 0)
async def main_read():
    logger.debug('main read called')

    return {"message": "main_read: Message sent"}