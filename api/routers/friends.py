from fastapi import APIRouter

from api.storage.friends import FriendStorage


class FriendsRouter(APIRouter):
    def __init__(self, friends_storage: FriendStorage):
        super().__init__()
        self.tags = ['friends']

        @self.post("/friends/{id}/add/{friend_id}")
        async def add_friendship(id: int, friend_id: int):
            return friends_storage.add_friend(id, friend_id)
