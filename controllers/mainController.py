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
			self.launch_tournament()
		if response == "2":
			self.manage_players()
		if response == "3":
			self.get_data()
		if response == "q":
			exit()
		elif response == "h":
			self.home()

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

	def manage_players(self):
		self.display.display_title("Gestion des joueurs")
		menu = {"1": "Créer un joueur", "2": "Liste des joueurs (ordre alphabétique)", "3": "Liste des joueurs (ordre de classement)"}
		response = self.display.display_menu(menu)
		if response == "1":
			self.create_player()
		if response == "2":
			self.get_players_sorted("alpha")
		if response == "3":
			self.get_players_sorted("rank")
		elif response == "h":
			self.home()
		self.manage_players()

	def create_tournament(self):
		self.display.display_title("Création d'un tournoi")
		menu = {"1": "Créer un joueur", "2": "Charger un joueur par son id", "3": "Charger un joueur par son nom"}
		response = self.display.display_menu(menu)
		if response == "1":
			self.create_player()
		if response == "2":
			self.select_player_by_id()
		if response == "3":
			self.select_player_by_name()
		elif response == "h":
			self.home()
		self.create_tournament()


	def select_player_by_id(self):
		index = self.display.verified_response("Veuillez entrer l'id du joueur: ", "^\d{1,4}$")
		self.display.display_player(Player.get_player_by_id(index))

	def select_player_by_name(self):
		first_name = self.display.verified_response("Veuillez entrer le prénom du joueur: ", "^[a-zA-Z]+$")
		last_name = self.display.verified_response("Veuillez entrer le nom du joueur: ", "^[a-zA-Z]+$")
		self.display.display_player(Player.get_player_by_name(first_name, last_name))

	def create_player(self):
		first_name = self.display.verified_response("Veuillez entrer le prénom: ", "^[a-zA-Z]+$")
		last_name = self.display.verified_response("Veuillez entrer le nom: ", "^[a-zA-Z]+$")
		birthdate = self.display.verified_response("Veuillez entrer la date de naissance (jj/mm/aaaa): ", "date")
		gender = self.display.verified_response("Veuillez entrer le genre (h-f-nb): ", "^(h|f|nb)$")
		rank = self.display.verified_response("Veuillez entrer le classement (score compris entre 100 et 9999: ", "^\d{3,4}$")

		player = Player(first_name, last_name, birthdate, gender, rank)
		player.save()

	def get_player_sSorted(self, sort_type):
		list_players = Player.sort_alpha() if sort_type == "alpha" else Player.sort_rank()
		self.display.display_list_players(list_players)

	def get_data(self):
		self.display.display_title("Toutes les données")
		menu = {"1": "Liste des joueurs (ordre alphabétique)", "2": "Liste des joueurs (ordre de classement)", "3": "Liste des tournois"}
		if response == "1":
			self.get_players_sorted("alpha")
		if response == "2":
			self.get_players_sorted("rank")
		if response == "3":
			self.getTournaments()
		elif response == "h":
			self.home()
