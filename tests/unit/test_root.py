from tests.unit.base import client


def test_root():
    response = client.get(url="/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
