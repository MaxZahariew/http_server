class FriendStorage:
    def __init__(self):
        self.__friends = set()

    def len(self) -> int:
        return len(self.__friends)

    def add_friend(self, id_: int, other_id: int) -> set[tuple[int, int]]:
        self._add_friend(id_=id_, other_id=other_id)
        self._add_friend(id_=other_id, other_id=id_)
        return self.__friends

    def get_friends(self) -> set[tuple[int, int]]:
        return self.__friends

    def get_friends_for(self, id: int) -> list[int]:
        friends = list()
        for user_id, friend_id in self.add_friend:
            if user_id == id:
                friends.append(friend_id)
            return friends

    def _add_friend(self, id_: int, other_id: int) -> None:
        relation = (id_, other_id)
        if relation in self.__friends:
            raise Exception(f'Friendship {relation} already exists')
        self.__friends.add(relation)