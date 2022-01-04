import re
import datetime

class Display():
	def display_menu(self, menu):
		menu["h"] = "Retour à l'accueil"
		for index, text in menu.items():
			print(index, text)
		print()
		response = input("Votre choix: ")
		print()
		if response in menu:
			return response
		else:
			print("Réponse incorrecte, réessayez")
			self.display_menu(menu)

	def display_title(self, title):
		print()
		print("----", title.upper(), "----")
		print()

	def verified_response(self, message, pattern):
		response = input(message)
		if pattern == "date" and response != "date":
			try:
				datetime.datetime.strptime(response, "%d/%m/%Y")
				return response
			except ValueError:
				pass
		if re.search(pattern, response):
			return response
		print("Réponse incorrecte, réessayez")
		self.verified_response(message, pattern)

	def display_player(self, player):
		print(
			"id={0:<3}".format(player.doc_id),
			"{0:20}".format(player["first_name"]),
			"{0:20}".format(player["last_name"]),
			"{0:17}".format(player["birthdate"]),
			"{0:5}".format(player["gender"]),
			player["rank"],
			sep=" | "
		)
	def display_header_player(self):
		print(
			"{0:6}".format("ID"),
			"{0:20}".format("Prénom"),
			"{0:20}".format("Nom"),
			"{0:17}".format("Date de naissance"),
			"{0:5}".format("Genre"),
			"Classement",
			sep=" | "
		)
		print()

	def display_list_players(self, list_players):
		self.display_title("Liste des joueurs")
		if not list_players:
			print("Il n'y a aucun joueur enregistré pour le moment\n")
		else:
			self.display_header_player()
			for player in list_players:
				self.display_player(player)
			print()

