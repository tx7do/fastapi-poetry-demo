from datetime import datetime

from tortoise import fields, models

from pydantic import *


class Status(BaseModel):
    """错误信息

    Attributes:
        code: 错误码。
        reason: 错误原因。
        message: 错误信息。
    """

    code: int
    reason: str
    message: str


class BaseModel(models.Model):
    """基础模型

    Attributes:
        id: 自增长ID
        created_at: 创建时间
        updated_at: 更新时间
        deleted_at: 删除时间
    """

    id = fields.IntField(pk=True, description="ID")

    created_at = fields.DatetimeField(auto_now_add=True, null=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, null=True, description="更新时间")
    deleted_at = fields.DatetimeField(null=True, description="删除时间")

    async def soft_delete(self):
        """软删除"""
        self.deleted_at = datetime.now()
        await self.save(update_fields=["deleted_at"])
