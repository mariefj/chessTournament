from views.main_view import Display
from .player_controller import PlayerController
from .tournament_controller import TournamentController


class MainController:
    def __init__(self):
        self.display = Display()
        # Passing self.home in parameters allows returning to principal menu
        self.playerController = PlayerController(self.home)
        self.tournamentController = TournamentController(self.home)

    def home(self):
        """ Display principal menu
        and does the right action according to user choice """
        self.display.display_title("Accueil")
        menu = {
            "1": "Lancer un tournoi",
            "2": "Gérer les joueurs",
            "3": "Accéder aux données",
            "q": "Quitter",
        }
        response = self.display.display_menu(menu)
        if response == "1":
            self.tournamentController.launch_tournament()
        if response == "2":
            self.playerController.manage_players()
        if response == "3":
            self.get_data()
        if response == "q":
            exit()
        elif response == "h":
            self.home()

    def get_data(self):
        """ Display data menu
        and does the right action according to user choice """
        self.display.display_title("Toutes les données")
        menu = {
            "1": "Liste des joueurs (ordre alphabétique)",
            "2": "Liste des joueurs (ordre de classement)",
            "3": "Liste des tournois",
        }
        response = self.display.display_menu(menu)
        if response == "1":
            self.playerController.get_players_sorted("alpha")
        if response == "2":
            self.playerController.get_players_sorted("rank")
        if response == "3":
            self.tournamentController.get_info_tournaments()
        elif response == "h":
            self.home()
        self.get_data()
