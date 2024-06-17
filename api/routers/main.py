from fastapi import APIRouter


router = APIRouter(prefix='/main')


@router.post("/create")
async def main_create():
    print('main create called')

    return {"message": "main_create: Message sent"}


@router.get("/read")
async def main_read():
    print('main read called')

    return {"message": "main_read: Message sent"}