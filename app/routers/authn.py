import uuid

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.authn import (
    LoginRequest,
    LoginResponse,
)
from ..models.user import User, login_with_password

router = APIRouter()


@router.post("/token", response_model=LoginResponse)
async def get_token_with_password(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await login_with_password(form_data.username, form_data.password)

    # 刷新令牌
    if user.refresh_token is None or user.refresh_token == "":
        user.refresh_token = uuid.uuid4()
        await User.filter(id=user.id).update(**{"refresh_token": user.refresh_token})

    return LoginResponse(
        id=user.id,
        account=user.account,
        name=user.name,
        access_token=user.get_access_token(),
        refresh_token=user.refresh_token.hex,
    )


@router.post("/login", response_model=LoginResponse, summary="前台账号登录")
async def login(form_data: LoginRequest):
    # 查询并校验密码
    user = await login_with_password(form_data.account, form_data.password)

    # 刷新令牌
    if user.refresh_token is None or user.refresh_token == "":
        user.refresh_token = uuid.uuid4()
        await User.filter(id=user.id).update(**{"refresh_token": user.refresh_token})

    return LoginResponse(
        id=user.id,
        account=user.account,
        name=user.name,
        access_token=user.get_access_token(),
        refresh_token=user.refresh_token.hex,
    )
