import datetime

from views.mainView import Display
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from .playerController import PlayerController



class TournamentController():

	def __init__(self, home):
		self.display = Display()
		self.home = home
		self.playerController = PlayerController(home)


	def launch_tournament(self):
		self.display.display_title("Gestion des tournois")
		menu = {"1": "Créer un tournoi", "2": "Charger un tournoi"}
		response = self.display.display_menu(menu)
		if response == "1":
			self.create_tournament()
		if response == "2":
			self.load_tournament()
		elif response == "h":
			self.home()
		self.launch_tournament()


	def create_tournament(self):
		self.display.display_title("Création d'un tournoi")
		name = input("Veuillez entrer le nom: ")
		location = input("Veuillez entrer le lieu: ")
		nb_rounds = self.display.verified_response("Veuillez entrer le nombre de tours: ", "^\d+$")
		time = self.display.verified_response("Veuillez entrer le temps de jeu: 1 bullet - 2 blitz - 3 rapide ", "^(1|2|3)$")
		if time == 1:
			time = "bullet"
		elif time == 2:
			time = "blitz"
		elif time == 3:
			time = "rapide"
		description = input("Veuillez entrer une description: ")
		list_rounds = []
		list_players = []

		tournament = Tournament(name, location, list_rounds, list_players, time, description, nb_rounds)
		tournament.save()


	def load_tournament(self):
		self.display.display_title("Chargement d'un tournoi")
		tournament = self.select_tournament_by_id()
		if len(tournament.list_rounds) == tournament.nb_rounds:
			self.display.display_message("Tournoi terminé")
			self.launch_tournament()
		if len(tournament.list_players) < 8:
			tournament = self.add_players(tournament)
		else:
			self.display.display_title("Lancement du tournoi !")
			self.play_swiss_system(tournament)

	def add_players(self, tournament):
		self.display.display_message("\nPour commencer le tournoi veuillez ajouter des joueurs")
		while len(tournament.list_players) < 8:
			player = self.playerController.choose_player()
			if player:
				if player.doc_id not in tournament.list_players:
					tournament.list_players.append(player.doc_id)
					tournament.save()
				else:
					self.display.display_message("Ce joueur a déjà été ajouté au tournoi")
		return tournament


	def select_tournament_by_id(self):
		id = self.display.verified_response("Veuillez entrer l'id du tournoi: ", "^\d+$")
		tournament = Tournament.get_tournament_by_id(int(id))
		if not tournament:
			self.display.display_message("Tournoi non trouvé, recommencez")
			return self.select_tournament_by_id()
		return Tournament(**tournament, doc_id=int(id))


	def sort_rank_round(self, list_players):
		list_players_for_round = []
		for id in list_players:
			player = Player.get_player_by_id(int(id))
			if player:
				list_players_for_round.append({"id": id, "rank": player["rank"], "score": 0})
		return sorted(list_players_for_round, key=lambda i: (i["rank"], i["id"]))


	def play_swiss_system(self, tournament):
		while len(tournament.list_rounds) < int(tournament.nb_rounds):
			is_round_starting = self.display.verified_response("Voulez-vous démarrer un tour ? 1: oui, je lance un nouveau tour - 2: non, retour au menu ", "^(1|2)$")
			if (is_round_starting == "2"):
				self.launch_tournament()
			else:
				nb_rounds_done = len(tournament.list_rounds)
				if nb_rounds_done == 0:
					list_players = self.sort_rank_round(tournament.list_players)
				else:
					last_round = tournament.list_rounds[nb_rounds_done - 1]
					list_players = sorted(last_round.list_players, key=lambda i: (i["score"], i["rank"], i["id"]))

				self.display.display_message("Début du tour")

				name = "Round " + str(nb_rounds_done + 1)
				list_games = self.get_list_games(list_players, tournament.list_rounds)

				self.display.display_title("Liste des matchs")
				for game in list_games:
					player_1 = Player.get_player_by_id(game[0][0])
					player_1 = Player(**player_1, doc_id=game[0][0])

					player_2 = Player.get_player_by_id(game[1][0])
					player_2 = Player(**player_2, doc_id=game[1][0])

					self.display.display_pairs_players(player_1, player_2)
				time_start = datetime.datetime.today()

				is_over = self.display.verified_response("Tapez 1 pour marquer le tour comme terminé: ", "^(1)$")
				if is_over:
					time_end = datetime.datetime.today()
					self.display.display_message("Fin du tour, veuillez rentrer les scores des joueurs: ")
					list_games = self.fill_scores(list_games)

				round = Round(name, list_games, time_start, time_end, is_over)
				tournament.list_rounds.append(Round.get_serialized_round(round))
				tournament.save()


	def get_list_all_pairs(self, list_rounds):
		list_pairs = []
		for round in list_rounds:
			for game in list_rounds.list_games:
				player_1 = game[0][0]
				player_2 = game[1][0]
				list_pairs.append((player_1, player_2))

		return list_pairs


	def get_list_games(self, list_players, list_rounds):
		half = len(list_players) // 2
		list_sup = list_players[:half]
		list_inf = list_players[half:]
		list_games = []
		i = 0
		j = 0
		while len(list_games) < (len(list_players) / 2):
			if len(list_rounds) > 0:
				list_pairs = self.get_list_pairs(list_rounds)
				pair = (list_sup[i]["id"], list_inf[j]["id"])
				while pair in list_pairs:
					j = j + 1
			player_1 = list_sup[i]
			player_2 = list_inf[j]
			print("player 1 = ", player_1)
			print("player 2 = ", player_2)
			list_games.append(([player_1["id"], player_1["score"]], [player_2["id"], player_2["score"]]))
			print("list_games = ", list_games)
			j = j + 1
			if j == len(list_inf):
				j = 0
			i = i + 1

		return list_games


	def fill_scores(self, list_games):
		for game in list_games:
			player_1 = Player.get_player_by_id(game[0][0])
			player_1 = Player(**player_1, doc_id=game[0][0])

			player_2 = Player.get_player_by_id(game[1][0])
			player_2 = Player(**player_2, doc_id=game[1][0])

			self.display.display_player_for_score(player_1)
			response_1 = self.display.verified_response("", "^(0|1|0.5)$")
			if response_1:
				game[0][1] = game[0][1] + float(response_1)
			self.display.display_player_for_score(player_2)
			response_2 = self.display.verified_response("", "^(0|1|0.5)$")
			if response_2:
				game[1][1] = game[1][1] + float(response_2)

		return list_games





