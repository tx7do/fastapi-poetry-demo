import pytest

from app.models import User, User_Pydantic


async def create_test_user() -> dict:
    user = {
        "id": 1,
        "account": "user1",
        "name": "王小明",
        "password": "password123"
    }
    await User.create(**user)
    return user


@pytest.mark.anyio
async def test_list_user():
    for i in range(1, 11):
        user = {
            "id": i,
            "account": 'user{}'.format(i),
            "name": '姓名{}'.format(i),
            "password": "password123"
        }
        await User.create(**user)

    users = await User.all()
    assert len(users) == 10


@pytest.mark.anyio
async def test_create_user():
    user = await create_test_user()

    data = await User_Pydantic.from_queryset_single(User.get(id=1))
    assert data.id == user['id']
    assert data.account == user['account']
    assert data.name == user['name']


@pytest.mark.anyio
async def test_update_user():
    await create_test_user()

    user = {
        "name": "石大壯"
    }
    await User.filter(id=1).update(**user)

    data = await User_Pydantic.from_queryset_single(User.get(id=1))
    assert data.name == user['name']


@pytest.mark.anyio
async def test_delete_user():
    await create_test_user()
    deleted_count = await User.filter(id=1).delete()
    assert deleted_count == 1
