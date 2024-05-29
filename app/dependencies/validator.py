import re

from fastapi import HTTPException, status

# 任意英文/任意数字/下划线/横线/减号
patternAccount = re.compile(r"^[a-zA-Z0-9_-]{4,16}$")
# 必须要包含任意英文和数字
patternPassword = re.compile(r"^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$")


def validate_account(account: str) -> bool:
    """验证输入的账号名是否合法

    Attributes:
        account: 账号
    """

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请输入账号",
        )

    if patternAccount.match(account) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="账号不合规，请输入：英文数字以及下划线、横线，4到16位",
        )

    return True


def validate_password(password: str) -> bool:
    """验证输入的明文密码是否合法

    Attributes:
        password: 密码
    """

    if password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请输入密码",
        )

    if patternPassword.match(password) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码不合规，请输入：包含任意英文和数字，8到16位",
        )

    return True
