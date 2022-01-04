import re
import datetime

class Display():
	def display_menu(self, menu):
		menu["h"] = "Retour à l'accueil"
		for index, text in menu.items():
			print(index, text)
		response = input("Votre choix: ")
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

	def display_list_players(self, list_players):
		if not list_players:
			print("Il n'y a aucun joueur enregistré pour le moment")
		else:
			for player in list_players:
				print("id={}".format(player.doc_id), player["first_name"], player["last_name"], player["birthdate"], player["gender"], player["rank"], sep=" | ")

