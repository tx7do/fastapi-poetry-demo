from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from .base import BaseModel


class User(BaseModel):
    account = fields.CharField(max_length=50, unique=True, description="账号名")
    password = fields.CharField(max_length=50, description="密码")
    name = fields.CharField(max_length=50, description="真实姓名")

    class Meta:
        table = "users"
        table_description = "账号表"

    class PydanticMeta:
        exclude = ["password"]


User_Pydantic = pydantic_model_creator(User)
User_Pydantic_List = pydantic_queryset_creator(User)
UserIn_Pydantic = pydantic_model_creator(User, exclude_readonly=True)
