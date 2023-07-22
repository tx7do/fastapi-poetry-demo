from fastapi import APIRouter

router = APIRouter()


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
