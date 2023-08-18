import re

from fastapi import HTTPException, status

# 任意英文/任意數字/下劃線/橫線/減號
patternAccount = re.compile(r"^[a-zA-Z0-9_-]{4,16}$")
# 必須要包含任意英文和數字
patternPassword = re.compile(r"^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,16}$")


def validate_account(account: str) -> bool:
    """驗證輸入的帳號名是否合法

    Attributes:
        account: 帳號名
    """

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="請輸入帳號",
        )

    if patternAccount.match(account) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="帳號不合規，請輸入：英文數字以及下劃線、橫線，4到16位",
        )

    return True


def validate_password(password: str) -> bool:
    """驗證輸入的明文密碼是否合法

    Attributes:
        password: 密碼
    """

    if password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="請輸入密碼",
        )

    if patternPassword.match(password) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密碼不合規，請輸入：包含任意英文和數字，8到16位",
        )

    return True
