import uuid

from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from ..dependencies import auth
from ..dependencies.db import BaseModel


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


User_Pydantic = pydantic_model_creator(User)
User_Pydantic_List = pydantic_queryset_creator(User)
UserIn_Pydantic = pydantic_model_creator(User, exclude_readonly=True)
