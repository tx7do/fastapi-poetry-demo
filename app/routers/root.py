from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary='根接口', description='根接口描述', tags=['根节点'])
async def root():
    return {"message": "Hello World"}
