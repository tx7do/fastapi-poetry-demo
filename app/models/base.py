from datetime import datetime

from tortoise import fields, models


class TimestampMixin:
    """时间戳混入类

    Attributes:
        created_at: 创建时间
        updated_at: 更新时间
        deleted_at: 删除时间
    """
    created_at = fields.DatetimeField(auto_now_add=True, null=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, null=True, description="更新时间")
    deleted_at = fields.DatetimeField(null=True, description="删除时间")


class NameMixin:
    """名称混入类

    Attributes:
        name: 名称
    """

    name = fields.CharField(max_length=50, unique=True, description="名称")


class CreatorMixin:
    """创建者混入类

    Attributes:
        created_by: 创建者账号名
    """
    created_by = fields.CharField(max_length=50, null=True, description="创建者账号名")


class UpdatorMixin:
    """更新者混入类

    Attributes:
        updated_by: 更新者账号名
    """
    updated_by = fields.CharField(max_length=50, null=True, description="更新者账号名")


class DeleterMixin:
    """删除者混入类

    Attributes:
        deleted_by: 删除者账号名
    """
    deleted_by = fields.CharField(max_length=50, null=True, description="删除者账号名")


class BaseModel(models.Model, TimestampMixin):
    """基础模型

    Attributes:
        id: 自增长ID
    """

    id = fields.IntField(pk=True, description="ID")

    class Meta:
        abstract = True

    async def soft_delete(self):
        """软删除"""
        self.deleted_at = datetime.now()
        await self.save(update_fields=["deleted_at"])
