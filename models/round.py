from tinydb import TinyDB, Query

class Round:
	def __init__(self, name, list_games, time_start, is_starting, is_over):
		self.name = name
		self.list_games = list_games
		self.time_start = time_start
		self.time_end = time_end
		self.is_starting = is_starting
		self.is_over = is_over
		self.list_rounds = TinyDB("db.json").table("rounds")


	def get_serialized_round(self):
		return {
			"name": self.name,
			"list_games": self.list_games,
			"time_start": self.time_start,
			"time_end": self.time_end,
			"is_starting": self.is_starting,
			"is_over": self.is_over,
		}