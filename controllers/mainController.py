from views.mainView import Display
from models.player import Player


class mainController():
	def __init__(self):
		self.display = Display()

	def home(self):
		self.display.display_title("Accueil")
		menu = {"1": "Lancer un tournoi", "2": "Gérer les joueurs", "3": "Accéder aux données", "q": "Quitter"}
		response = self.display.display_menu(menu)
		if response == "1":
			self.launchTournament()
		if response == "2":
			self.managePlayers()
		if response == "3":
			self.getData()
		if response == "q":
			exit()
		elif response == "h":
			self.home()

	def launchTournament(self):
		self.display.display_title("Gestion du tournoi")
		menu = {"1": "Créer un tournoi", "2": "Charger un tournoi"}
		self.display.display_menu(menu)

	def managePlayers(self):
		self.display.display_title("Gestion des joueurs")
		menu = {"1": "Créer un joueur", "2": "Voir les joueurs par ordre alphabétique", "3": "Voir les joueurs par ordre de classement"}
		response = self.display.display_menu(menu)
		if response == "1":
			self.createPlayer()
		if response == "2":
			self.getPlayersSorted("alpha")
		if response == "3":
			self.getPlayersSorted("rank")
		elif response == "h":
			self.home()

	def createPlayer(self):
		first_name = self.display.verified_response("Veuillez entrer le prénom: ", "^[a-zA-Z]+$")
		last_name = self.display.verified_response("Veuillez entrer le nom: ", "^[a-zA-Z]+$")
		birthdate = self.display.verified_response("Veuillez entrer la date de naissance (jj/mm/aaaa): ", "date")
		gender = self.display.verified_response("Veuillez entrer le genre (h-f-nb): ", "^(h|f|nb)$")
		rank = self.display.verified_response("Veuillez entrer le classement (score compris entre 100 et 9999: ", "^\d{3,4}$")

		player = Player(first_name, last_name, birthdate, gender, rank)
		player.save()

	def getPlayersSorted(self, sort_type):
		list_players = Player.sortAlpha() if sort_type == "alpha" else Player.sortRank()
		self.display.display_list_players(list_players)

	def getData(self):
		self.display.display_title("Toutes les données")
		menu = {"1": "Liste des joueurs", "2": "Liste des tournois", "3": "Voir les données d'un tournoi"}
