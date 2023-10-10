from fastapi import APIRouter
from typing import List
from starlette.status import HTTP_204_NO_CONTENT

from app.dependencies.exceptions import HTTP_404_NOT_FOUND
from app.models.user import User
from app.schemas.user import User_Pydantic, UserIn_Pydantic

router = APIRouter()


@router.get("/users", response_model=List[User_Pydantic], summary='获取账号列表')
async def get_users():
    return await User_Pydantic.from_queryset(User.all())


@router.get("/users/{user_id}", response_model=User_Pydantic, summary='获取一个账号的信息')
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@router.post("/users", response_model=User_Pydantic, summary='創建一个账号')
async def create_user(user: UserIn_Pydantic):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.put("/users/{user_id}", response_model=User_Pydantic, summary='修改一个账号的信息')
async def update_user(user_id: int, user: UserIn_Pydantic):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT, summary='刪除一个账号')
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTP_404_NOT_FOUND
