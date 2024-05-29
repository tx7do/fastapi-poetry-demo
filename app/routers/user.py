from fastapi import APIRouter
from fastapi.params import Depends
from typing import List
from starlette.status import HTTP_204_NO_CONTENT

from app.dependencies.exceptions import HTTP_404_NOT_FOUND
from app.models.user import User, extract_user_token
from app.schemas.user import User_Pydantic, UserIn_Pydantic

router = APIRouter()


@router.get("/users", response_model=List[User_Pydantic], summary='获取账号列表')
async def get_users(_: User = Depends(extract_user_token)):
    return await User_Pydantic.from_queryset(User.all())


@router.get("/users/{user_id}", response_model=User_Pydantic, summary='获取一个账号的信息')
async def get_user(user_id: int, _: User = Depends(extract_user_token)):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@router.post("/users", response_model=User_Pydantic, summary='創建一个账号')
async def create_user(user: UserIn_Pydantic, _: User = Depends(extract_user_token)):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.put("/users/{user_id}", response_model=User_Pydantic, summary='修改一个账号的信息')
async def update_user(user_id: int, user: UserIn_Pydantic, _: User = Depends(extract_user_token)):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT, summary='刪除一个账号')
async def delete_user(user_id: int, _: User = Depends(extract_user_token)):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTP_404_NOT_FOUND


@router.get("/users/me", summary='读取当前登录用户')
async def read_users_me(current_user: User = Depends(extract_user_token)):
    return current_user
