import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import auth, exceptions
from ..dependencies.auth import login_with_password
from ..models.authn import (
    RefreshTokenResponse,
    RefreshTokenRequest,
    LoginRequest,
    LoginResponse,
    ManagerLoginResponse,
)
from ..models.user import User

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


@router.post("/login", response_model=LoginResponse, summary="前台帳號登入")
async def login(form_data: LoginRequest):
    # 查詢並且校驗密碼
    user = await auth.login_with_password(form_data.account, form_data.password)

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
