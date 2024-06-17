from fastapi import APIRouter
from fastapi_versioning import version


router = APIRouter(prefix='/main')


@router.post("/create")
@version(2, 0)
async def main_create():
    print('main create called')

    return {"message": "v2.0: main_create: Message sent"}


@router.get("/read")
@version(2, 0)
async def main_read():
    print('main read called')

    return {"message": "v2.0: main_read: Message sent"}
