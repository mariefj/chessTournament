from views.main_view import Display
from models.player import Player


class PlayerController:
    def __init__(self, home):
        self.display = Display()
        self.home = home

    def manage_players(self):
        """ Display player principal menu
        and does the right action according to user choice """
        self.display.display_title("Gestion des joueurs")
        menu = {
            "1": "Créer un joueur",
            "2": "Liste des joueurs (ordre alphabétique)",
            "3": "Liste des joueurs (ordre de classement)",
        }
        response = self.display.display_menu(menu)
        if response == "1":
            self.create_player()
        if response == "2":
            self.get_players_sorted("alpha")
            self.modify_player()
        if response == "3":
            self.get_players_sorted("rank")
            self.modify_player()
        elif response == "h":
            self.home()
        self.manage_players()

    def choose_player(self):
        """ Display player management menu
        and returns the chosen Player's instance """
        menu = {
            "1": "Créer un joueur",
            "2": "Charger un joueur par son id",
            "3": "Charger un joueur par son nom",
        }
        response = self.display.display_menu(menu)
        if response == "1":
            return self.create_player()
        if response == "2":
            self.get_players_sorted("alpha")
            return self.select_player_by_id()
        if response == "3":
            self.get_players_sorted("alpha")
            return self.select_player_by_name()
        elif response == "h":
            self.home()
        self.choose_player()

    def select_player_by_id(self):
        """ Returns a Player's instance
        according to the chosen id by user """
        id = self.display.verified_response(
                "Veuillez entrer l'id du joueur: ",
                r"^\d+$"
        )
        player = Player.get_player_by_id(int(id))
        if not player:
            self.display.display_message("Joueur non trouvé, recommencez")

            return self.select_player_by_id()

        return Player(**player, doc_id=int(id))

    def select_player_by_name(self):
        """ Returns a Player's instance
        according to the chosen name info by user """
        first_name = self.display.verified_response(
            "Veuillez entrer le prénom du joueur: ", "^[a-zA-Z]+$"
        )
        last_name = self.display.verified_response(
            "Veuillez entrer le nom du joueur: ", "^[a-zA-Z]+$"
        )

        list_matches = Player.get_player_by_name(first_name, last_name)
        if list_matches == []:
            self.display.display_message("Joueur non trouvé, recommencez")

            return self.select_player_by_name()
        elif len(list_matches) == 1:
            player = list_matches[0]
            id = Player.get_player_with_right_doc_id(Player(**player)).doc_id

            return Player(**player, doc_id=int(id))
        else:
            self.display.display_list_players(list_matches)

            return self.select_player_by_id()

    def create_player(self):
        """ Create a new player in database
        and returns a Player's instance of this new player """
        first_name = self.display.verified_response(
            "Veuillez entrer le prénom: ", "^[a-zA-Z]+$"
        )
        last_name = self.display.verified_response(
            "Veuillez entrer le nom: ", "^[a-zA-Z]+$"
        )
        birthdate = self.display.verified_response(
            "Veuillez entrer la date de naissance (jj/mm/aaaa): ", "date"
        )
        gender = self.display.verified_response(
            "Veuillez entrer le genre (h-f-nb): ", "^(h|f|nb)$"
        )
        rank = self.display.verified_response(
            "Veuillez entrer le classement (score compris entre 100 et 9999: ",
            r"^\d{3,4}$",
        )

        player = Player(first_name, last_name, birthdate, gender, rank)
        player.save()

        # Necessary to search for the new player added
        # to get a player with doc_id attribute
        return Player.get_player_with_right_doc_id(player)

    def get_players_sorted(self, sort_type):
        """ Display list of players
        sorted according to sort_type parameter given """
        list_players = (
            Player.sort_alpha() if sort_type == "alpha" else Player.sort_rank()
        )
        self.display.display_list_players(list_players)

    def modify_player(self):
        """ Manage a player's rank update """
        response = self.display.verified_response(
            "Souhaitez vous changer le classement d'un joueur ? "
            "1: oui 2: non\n",
            "^(1|2)$",
        )
        if response == "1":
            self.display.display_message(
                "Choisissez l'id d'un joueur pour changer son classement"
            )
            player = self.select_player_by_id()
            rank = self.display.verified_response(
                "Veuillez entrer le classement "
                "(score compris entre 100 et 9999: ",
                r"^\d{3,4}$",
            )

            player.rank = rank
            player.save()
        if response == "2":
            self.manage_players()
