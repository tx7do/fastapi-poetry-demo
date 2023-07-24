from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from .base import BaseModel


class User(BaseModel):
    name = fields.TextField()

    def __str__(self):
        return self.name


User_Pydantic = pydantic_model_creator(User)
User_Pydantic_List = pydantic_queryset_creator(User)
UserIn_Pydantic = pydantic_model_creator(User, exclude_readonly=True)
