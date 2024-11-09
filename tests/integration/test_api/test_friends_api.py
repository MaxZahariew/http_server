from http import HTTPStatus

import pytest
from starlette.testclient import TestClient

from api.storage.friends import FriendStorage


class TestFriendApi:
    @pytest.mark.parametrize(
        "user_id, friend_id",
        [
            (0, 1),
            (42, 21),
            (0, 0),
        ],
    )
    def test_add_friend(
        self,
        client: TestClient,
        user_id: int,
        friend_id: int,
        friends_storage: FriendStorage,
    ):
        res = client.post(f"/friends/{user_id}/add/{friend_id}")

        assert res.status_code == HTTPStatus.OK
        assert friends_storage.get_friends() == {(user_id, friend_id)}
