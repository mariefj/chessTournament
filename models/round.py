from tinydb import TinyDB, Query

class Round:
	def __init__(self, name, list_games, player_1, player_2, score_player_1, score_player_2, time_start, is_starting, is_over, is_starting):
		self.name = name
		self.list_games = list_games
		self.player_1 = player_1
		self.player_2 = player_2
		self.score_player_1 = score_player_1
		self.score_player_2 = score_player_2
		self.time_start = time_start
		self.time_end = time_end
		self.is_over = is_over
		self.is_starting = is_starting
		self.db = TinyDB("data/round.json")

	def get_serialized_round(self):
		return {
			"name": self.name,
			"player_1": self.player_1,
			"player_2": self.player_2,
			"score_player_1": self.score_player_1,
			"score_player_2": self.score_player_2,
			"time_start": self.time_start,
			"time_end": self.time_end,
			"is_over": self.is_over,
			"is_starting": self.is_starting,
		}