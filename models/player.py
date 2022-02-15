from tinydb import TinyDB, Query


class Player:
    def __init__(
        self,
        first_name,
        last_name,
        birthdate,
        gender,
        rank=0,
        score=0,
        doc_id=0
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.gender = gender
        self.rank = rank
        self.score = score
        self.doc_id = doc_id
        self.list_players = TinyDB("db.json").table("players")

    def get_serialized_player(self):
        return {
            "first_name": self.first_name.lower(),
            "last_name": self.last_name.lower(),
            "birthdate": self.birthdate,
            "gender": self.gender,
            "rank": self.rank,
            "score": self.score,
        }

    def save(self):
        if self.doc_id:
            self.list_players.update(
                self.get_serialized_player(), doc_ids=[self.doc_id]
            )
        else:
            self.list_players.insert(self.get_serialized_player())

    @staticmethod
    def get_all_players():
        return TinyDB("db.json").table("players").all()

    @staticmethod
    def get_player_by_id(id):
        return TinyDB("db.json").table("players").get(doc_id=id)

    @staticmethod
    def get_player_by_name(first_name, last_name):
        return (
            TinyDB("db.json")
            .table("players")
            .search(
                (Query().first_name == first_name.lower())
                & (Query().last_name == last_name.lower())
            )
        )

    @staticmethod
    def get_player_with_right_doc_id(player):
        return (
            TinyDB("db.json")
            .table("players")
            .search(
                (Query().first_name == player.first_name.lower())
                & (Query().last_name == player.last_name.lower())
                & (Query().birthdate == player.birthdate)
                & (Query().rank == player.rank)
            )[0]
        )

    @staticmethod
    def sort_alpha():
        list_players = Player.get_all_players()
        return sorted(
            list_players,
            key=lambda i: (i["last_name"], i["first_name"], i["rank"])
        )

    @staticmethod
    def sort_rank():
        list_players = Player.get_all_players()
        return sorted(
            list_players,
            key=lambda i: (i["rank"], i["last_name"], i["first_name"])
        )
