from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.dependencies import validator as validate


class RefreshTokenRequest(BaseModel):
    """刷新令牌请求
    """

    refresh_token: str = Field(description="刷新令牌")


class RefreshTokenResponse(BaseModel):
    """刷新令牌回复
    """

    token_type: str = Field(default="bearer", description="令牌类型，默认为：bearer")
    access_token: str = Field(description="JWT令牌")
    refresh_token: str = Field(description="刷新令牌")


class LoginRequest(BaseModel):
    """登录请求
    """

    account: str = Field(description="账号")
    password: str = Field(description="密码")

    class Config:
        json_schema_extra = {
            "example": {
                "account": "user1",
                "password": "password12345"
            }
        }

    @field_validator("account")
    def validate_account(cls, value):
        if validate.validate_account(value):
            return value

    @field_validator("password")
    def validate_password(cls, value):
        if validate.validate_password(value):
            return value


class LoginResponse(BaseModel):
    """登录结果返回值
    """

    id: int = Field(description="账号ID")
    account: str = Field(description="账号")
    token_type: str = Field(default="bearer", description="令牌类型，默认为：bearer")
    access_token: str = Field(description="JWT令牌")
    refresh_token: Optional[str] = Field(default=None, description="刷新令牌")


class ManagerLoginResponse(BaseModel):
    """后端登录结果返回值
    """

    id: int = Field(description="账号ID")
    account: str = Field(description="账号")
    token_type: str = Field(default="bearer", description="令牌类型，默认为：bearer")
    access_token: str = Field(description="JWT令牌")
    refresh_token: Optional[str] = Field(default=None, description="刷新令牌")
