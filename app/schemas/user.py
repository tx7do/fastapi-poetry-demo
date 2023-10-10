from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from app.models import User

User_Pydantic = pydantic_model_creator(User)
User_Pydantic_List = pydantic_queryset_creator(User)
UserIn_Pydantic = pydantic_model_creator(User, exclude_readonly=True)
