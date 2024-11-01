import pytest
from starlette.testclient import TestClient
from http import HTTPStatus

from api.models.api.new_user import NewUser
from api.models.api.user import User
from api.models.db.user import User as DBUser
from api.storage.users import UserStorage


@pytest.fixture()
def new_user() -> NewUser:
    return NewUser(
        name="Imax", age=38, email="Imax@mail.ru", about="It,s me", password="rs485"
    )


@pytest.fixture()
def test_user(new_user: NewUser) -> User:
    return User(
        id=0,
        name=new_user.name,
        age=new_user.age,
        email=new_user.email,
        about=new_user.about,
        password=new_user.password,
    )

@pytest.fixture()
def db_user(test_user: User) -> DBUser:
    return DBUser(
        id=test_user.id,
        name=test_user.name,
        age=test_user.age,
        email=test_user.email,
        about=test_user.about,
        password=test_user.password,
    )


class TestUserAPI:

    def test_get_users(self, client: TestClient):
        res = client.get("/users")

        assert res.status_code == HTTPStatus.OK

    def test_create_user(
        self, client: TestClient, test_user: User, new_user: NewUser, db_user: DBUser
    ):
        expected_user = db_user
        res = client.post("/users", json=new_user.model_dump())

        assert res.status_code == HTTPStatus.OK
        assert res.json() == expected_user
        