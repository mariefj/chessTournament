from tinydb import TinyDB, Query

class Tournament:
	def __init__(self, name, location, list_rounds, list_players, time, description, nb_rounds=4,):
		self.name = name
		self.location = location
		self.nb_rounds = nb_rounds
		self.list_rounds = list_rounds
		self.list_players = list_players
		self.time = time
		self.description = description
		self.db = TinyDB("data/tournament.json")

	def get_serialized_tournament(self):
		return {
			"name": self.name,
			"location": self.location,
			"nb_rounds": self.nb_rounds,
			"list_rounds": self.list_rounds,
			"list_players": self.list_players,
			"time": self.time,
			"description": self.description,
		}