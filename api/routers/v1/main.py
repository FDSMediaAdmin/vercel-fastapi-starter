from fastapi import APIRouter, Depends
from fastapi_versioning import version

from loguru import logger

from shared.decorator.is_request_from_rapid_api import is_request_from_rapid_api

router = APIRouter(prefix='/main')


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
