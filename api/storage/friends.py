class FriendStorage:
    def __init__(self):
        self.__friends = set()

    def len(self) -> int:
        return len(self.__friends)

    def add_friend(self, id_: int, other_id: int) -> set[tuple[int, int]]:
        relation = (id_, other_id)
        if relation in self.__friends:
            raise Exception(f"Friendship {relation} already exists")
        self.__friends.add(relation)
        return self.__friends

    def get_friends(self) -> set[tuple[int, int]]:
        return self.__friends
