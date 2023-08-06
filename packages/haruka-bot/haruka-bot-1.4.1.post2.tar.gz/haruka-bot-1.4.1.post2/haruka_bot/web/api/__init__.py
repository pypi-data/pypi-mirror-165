from fastapi import APIRouter

from ...database import DB as db

router = APIRouter(tags=["api"])


# @router.get("/")
# async def root():
#     return {"message": "Hello World"}


@router.get("/sub_list")
async def sub_list(type: str, type_id: int):
    return dict((await db.get_sub_list(type, type_id))[0])
