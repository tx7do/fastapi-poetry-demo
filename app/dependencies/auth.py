from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from ..configs.auth import get_auth_settings
from ..models.user import User
from .exceptions import HTTP_401_UNAUTHORIZED

auth_settings = get_auth_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    # print(password, pwd_context.hash(password))
    return pwd_context.hash(password)


async def login_with_password(account: str, password: str) -> User:
    """账号密码登录

    Attributes:
        account: 账号名
        password: 明文密码
    """

    user = await User.get_active_user(account=account)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="账号不存在",
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def create_access_token(*, data: dict) -> str:
    """创建JWT令牌

    :param data:
    :return:
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, auth_settings.AUTH_SECRET_KEY, algorithm=auth_settings.AUTH_ALGORITHM
    )
    return encoded_jwt


async def extract_user_token(token: str = Depends(oauth2_scheme)) -> User:
    """从JWT令牌中解析出用户信息

    :param token: JWT令牌
    :return: 用户信息
    """

    try:
        payload = jwt.decode(
            token,
            auth_settings.AUTH_SECRET_KEY,
            algorithms=[auth_settings.AUTH_ALGORITHM],
        )
        user = await User.get_active_user(account=payload.get("account"))
    except jwt.PyJWTError:
        raise HTTP_401_UNAUTHORIZED
    if not user:
        raise HTTP_401_UNAUTHORIZED
    return user
