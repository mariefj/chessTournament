from tinydb import TinyDB, Query
from operator import attrgetter

class Player:
	def __init__(self, first_name, last_name, birthdate, gender, rank=0):
		self.first_name = first_name
		self.last_name = last_name
		self.birthdate = birthdate
		self.gender = gender
		self.rank = rank
		self.list_players = TinyDB("db.json").table("players")

	def get_serialized_player(self):
		return {
			"first_name": self.first_name,
			"last_name": self.last_name,
			"birthdate": self.birthdate,
			"gender": self.gender,
			"rank": self.rank,
		}

	def save(self):
		self.list_players.insert(self.get_serialized_player())

	@staticmethod
	def get_all_players():
		return TinyDB("db.json").table("players").all()

	@staticmethod
	def sortAlpha():
		list_players = Player.get_all_players()
		return sorted(list_players, key=lambda i: (i["last_name"], i["first_name"], i["rank"]))

	@staticmethod
	def sortRank():
		list_players = Player.get_all_players()
		return sorted(list_players, key=lambda i: (i["rank"], i["last_name"], i["first_name"]))
