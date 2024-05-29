from fastapi import APIRouter

router = APIRouter()


@router.get("/", summary='根接口', description='根接口描述')
async def root():
    return {"message": "Hello World"}
