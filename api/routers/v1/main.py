from fastapi import APIRouter
from fastapi_versioning import version

from loguru import logger

router = APIRouter(prefix='/main')


@router.post("/create")
@version(1, 0)
async def main_create():
    logger.debug('main create called')

    return {"message": "main_create: Message sent"}


@router.get("/read")
@version(1, 0)
async def main_read():
    logger.debug('main read called')

    return {"message": "main_read: Message sent"}