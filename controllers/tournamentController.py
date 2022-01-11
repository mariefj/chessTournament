from views.mainView import Display
from models.player import Player
from models.tournament import Tournament


class TournamentController():

	def __init__(self, home):
		self.display = Display()
		self.home = home


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

	def create_tournament(self):
		self.display.display_title("Création d'un tournoi")
		name = self.display.verified_response("Veuillez entrer le nom: ", "^[a-zA-Z]+$")
		location = self.display.verified_response("Veuillez entrer le lieu: ", "^[a-zA-Z]+$")
		nb_rounds = self.display.verified_response("Veuillez entrer le nombre de tours: ", "^\d+$")
		time = self.display.verified_response("Veuillez entrer le temps de jeu: ", "^(3|5|15|60)$")
		description = self.display.verified_response("Veuillez entrer une description: ", "^[a-zA-Z]+$")
		list_rounds = []
		list_players = []

		tournament = Tournament(name, location, list_rounds, list_players, time, description, nb_rounds)
		tournament.save()
