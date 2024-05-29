import uuid
import jwt

from tortoise import fields
from fastapi import HTTPException, status, Depends

from ..dependencies import auth
from ..dependencies.db import BaseModel
from ..dependencies.auth import oauth2_scheme
from ..dependencies.exceptions import HTTP_401_UNAUTHORIZED


class User(BaseModel):
    account = fields.CharField(max_length=50, unique=True, description="账号名")
    password = fields.CharField(max_length=50, description="密码")
    name = fields.CharField(max_length=50, description="真实姓名")

    class Meta:
        table = "users"
        table_description = "账号表"

    class PydanticMeta:
        exclude = ["password"]

    @classmethod
    async def get_active_user(cls, user_id: int = None, account: str = None):
        if user_id is not None:
            return await cls.get_or_none(id=user_id, deleted_at=None)
        if account is not None:
            return await cls.get_or_none(account=account, deleted_at=None)
        return None

    @classmethod
    def create(cls, **kwargs):
        kwargs["password"] = auth.get_password_hash(kwargs["password"])
        kwargs["refresh_token"] = uuid.uuid4().hex
        return super().create(**kwargs)

    def get_access_token(self):
        return auth.create_access_token(data={"sub": self.id, "account": self.account})


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

    if not auth.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user(token: str):
    """从JWT令牌中解析出用户信息
    :return: 用户信息
    """

    try:
        payload = await auth.extract_access_token(token)
        user = await User.get_active_user(account=payload.get("account"))
    except jwt.PyJWTError:
        raise HTTP_401_UNAUTHORIZED
    if not user:
        raise HTTP_401_UNAUTHORIZED
    return user


async def extract_user_token(token: str = Depends(oauth2_scheme)) -> User:
    """从JWT令牌中解析出用户信息
    :return: 用户信息
    """

    return await get_current_user(token)
