from tinydb import TinyDB


class Tournament:
    def __init__(
        self,
        name,
        location,
        list_rounds,
        list_players,
        time,
        description,
        nb_rounds=4,
        doc_id=0,
        is_over=0,
    ):
        self.name = name
        self.location = location
        self.nb_rounds = nb_rounds
        self.list_rounds = list_rounds
        self.list_players = list_players
        self.time = time
        self.description = description
        self.list_tournaments = TinyDB("db.json").table("tournaments")
        self.doc_id = doc_id
        self.is_over = is_over

    def get_serialized_tournament(self):
        return {
            "name": self.name,
            "location": self.location,
            "nb_rounds": self.nb_rounds,
            "list_rounds": self.list_rounds,
            "list_players": self.list_players,
            "time": self.time,
            "description": self.description,
            "is_over": self.is_over,
        }

    def save(self):
        if self.doc_id:
            self.list_tournaments.update(
                self.get_serialized_tournament(), doc_ids=[self.doc_id]
            )
        else:
            self.list_tournaments.insert(self.get_serialized_tournament())

    @staticmethod
    def get_all_tournaments():
        return TinyDB("db.json").table("tournaments").all()

    @staticmethod
    def get_tournament_by_id(id):
        return TinyDB("db.json").table("tournaments").get(doc_id=id)
