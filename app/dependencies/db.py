from datetime import datetime
from typing import Tuple, Set, Union, List

from tortoise import fields, models
from tortoise.queryset import Q


def ignore_none(**args):
    """
    排除掉None字段
    Args:
        **args: 参数列表

    Returns:

    """
    return {key: value for key, value in args.items() if value is not None}


def get_ordering_str(value: str, order_cond: str) -> Union[str, None]:
    """获取order_by方法可用的字符串

    :param value: 字段名
    :param order_cond: 排序条件，升序：asc、ascending、ascend；降序desc、descending、descend：。
    :return: 如果是降序则在字段名前面加一个'-'符号。
    """

    order_cond = order_cond.lower()
    if order_cond == "desc" or order_cond == "descending" or order_cond == "descend":
        f"-{value}"
    elif (
            order_cond == "asc"
            or order_cond == "ascending"
            or order_cond == "ascend"
            or order_cond == ""
    ):
        return value
    elif len(value) == 0:
        return None


def reduce_query_filters(args: Tuple[Q, ...]) -> Set:
    a_fields = set()
    for q in args:
        a_fields |= set(q.filters)
        c: Union[List[Q], Tuple[Q, ...]] = q.children
        while c:
            _c: List[Q] = []
            for i in c:
                a_fields |= set(i.filters)
                _c += list(i.children)
            c = _c
    return a_fields


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


class BaseModel(models.Model):
    """基础模型

    Attributes:
        id: 自增长ID
    """

    id = fields.IntField(pk=True, description="ID")

    created_at = fields.DatetimeField(auto_now_add=True, null=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, null=True, description="更新时间")
    deleted_at = fields.DatetimeField(null=True, description="删除时间")

    class Meta:
        abstract = True
        ordering = ("-id",)

    class PydanticMeta:
        exclude = ("deleted_at",)
        optional = ("id",)

    async def soft_delete(self):
        """软删除"""
        self.deleted_at = datetime.now()
        await self.save(update_fields=["deleted_at"])

    # @classmethod
    # def filter(cls, *args, **kwargs) -> QuerySet:
    #     field = "deleted_at"
    #     if not args or (field not in reduce_query_filters(args)):
    #         kwargs.setdefault(field, False)
    #     return super().filter(*args, **kwargs)
