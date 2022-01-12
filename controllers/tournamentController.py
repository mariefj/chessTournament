from views.mainView import Display
from models.player import Player
from models.tournament import Tournament
from .playerController import PlayerController


class TournamentController():

	def __init__(self, home):
		self.display = Display()
		self.home = home
		self.playerController = PlayerController(home)


	def launch_tournament(self):
		self.display.display_title("Gestion du tournoi")
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
		time = self.display.verified_response("Veuillez entrer le temps de jeu: ", "^(1|3|5|15|60)$")
		description = input("Veuillez entrer une description: ")
		list_rounds = []
		list_players = []

		tournament = Tournament(name, location, list_rounds, list_players, time, description, nb_rounds)
		tournament.save()


	def load_tournament(self):
		self.display.display_title("Chargement d'un tournoi")
		tournament = self.select_tournament_by_id()
		if len(tournament.list_players) < 8:
			self.display.display_message("\nPour commencer le tournoi veuillez ajouter des joueurs")
		while len(tournament.list_players) < 8:
			player = self.playerController.choose_player()
			if player:
				if player.doc_id not in tournament.list_players:
					tournament.list_players.append(player.doc_id)
					tournament.save()
				else:
					self.display.display_message("Ce joueur a déjà été ajouté au tournoi")


	def select_tournament_by_id(self):
		id = self.display.verified_response("Veuillez entrer l'id du tournoi: ", "^\d+$")
		tournament = Tournament.get_tournament_by_id(int(id))
		if not tournament:
			self.display.display_message("Tournoi non trouvé, recommencez")
			return self.select_tournament_by_id()
		return Tournament(**tournament, doc_id=int(id))
