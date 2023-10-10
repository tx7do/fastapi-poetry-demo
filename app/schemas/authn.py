from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.dependencies import validator as validate


class RefreshTokenRequest(BaseModel):
    """刷新令牌請求
    """

    refresh_token: str = Field(description="刷新用令牌")


class RefreshTokenResponse(BaseModel):
    """刷新令牌回復
    """

    token_type: str = Field(default="bearer", description="令牌類型，默認為：bearer")
    access_token: str = Field(description="JWT令牌")
    refresh_token: str = Field(description="刷新用令牌")


class LoginRequest(BaseModel):
    """登錄請求
    """

    account: str = Field(description="帳號")
    password: str = Field(description="密碼")

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
    """登錄結果返回值
    """

    id: int = Field(description="帳號id")
    account: str = Field(description="帳號")
    token_type: str = Field(default="bearer", description="令牌類型，默認為：bearer")
    access_token: str = Field(description="JWT令牌")
    refresh_token: Optional[str] = Field(default=None, description="刷新用令牌")


class ManagerLoginResponse(BaseModel):
    """登錄結果返回值
    """

    id: int = Field(description="帳號id")
    account: str = Field(description="帳號")
    token_type: str = Field(default="bearer", description="令牌類型，默認為：bearer")
    access_token: str = Field(description="JWT令牌")
    refresh_token: Optional[str] = Field(default=None, description="刷新用令牌")
