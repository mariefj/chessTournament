import re
import datetime


class Display:

    # ******************GENERAL*************************************

    def display_message(self, message):
        print(message)

    def display_menu(self, menu):
        """ Display menu as a list of items in the list given in parameter
        and returns response from user """
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
            return self.display_menu(menu)

    def display_title(self, title):
        print()
        print("----", title.upper(), "----")
        print()

    def verified_response(self, message, pattern):
        """
        Returns response from input

            Parameters:
                message (str): a string to display with input
                pattern (str): regex exp or "date" to check response

            Returns:
                response/self.verified_response: response given by user
        """
        response = input(message)
        if pattern == "date" and response != "date":
            try:
                datetime.datetime.strptime(response, "%d/%m/%Y")
                return response
            except ValueError:
                pass
        if re.search(pattern, response):
            return response
        else:
            print("Réponse incorrecte, réessayez")
            return self.verified_response(message, pattern)

    # *****************************************************************

    # ******************PLAYER*****************************************

    def display_player(self, player):
        """ Display player's info where player is a dictionary from database"""
        print(
            "id={:<3}".format(player.doc_id),
            "{:20}".format(player["first_name"]),
            "{:20}".format(player["last_name"]),
            "{:17}".format(player["birthdate"]),
            "{:5}".format(player["gender"]),
            player["rank"],
            sep=" | ",
        )

    def display_player_object(self, player):
        """ Display player's info where player is a Player's instance"""
        print(
            "id={:<3}".format(player.doc_id),
            "{:20}".format(player.first_name),
            "{:20}".format(player.last_name),
            "{:17}".format(player.birthdate),
            "{:5}".format(player.gender),
            "{:5}".format(player.score),
            player.rank,
            sep=" | ",
        )

    def display_header_player(self):
        print(
            "{:6}".format("ID"),
            "{:20}".format("Prénom"),
            "{:20}".format("Nom"),
            "{:17}".format("Date de naissance"),
            "{:5}".format("Genre"),
            "Classement",
            sep=" | ",
        )
        print()

    def display_list_players(self, list_players):
        """ Display the players of the list_players given as parameter """
        self.display_title("Liste des joueurs")
        if not list_players:
            print("Il n'y a aucun joueur enregistré pour le moment\n")
        else:
            self.display_header_player()
            for player in list_players:
                self.display_player(player)
            print()

    def display_pairs_players(self, player_1, player_2):
        """ Display match info with the two players given as parameters """
        message = (
            "Match opposant les joueurs "
            + str(player_1.first_name)
            + " "
            + str(player_1.last_name)
            + " id ("
            + str(player_1.doc_id)
            + ")"
            + " et "
            + str(player_2.first_name)
            + " "
            + str(player_2.last_name)
            + " id ("
            + str(player_2.doc_id)
            + ")"
        )
        print(message)
        print()

    def display_player_for_score(self, player):
        """ Display adding score for the player given as parameter """
        print()
        print(
            "Score du joueur ",
            player.first_name,
            " ",
            player.last_name,
            " id (",
            player.doc_id,
            ") (score possible 0 / 1 / 0.5) : ",
        )

    # *************************************************************

    # ******************TOURNAMENT*********************************

    def display_tournament(self, tournament):
        """ Display tournament's info
        where tournament is a dictionary from database"""
        print(
            "id={:<3}".format(tournament.doc_id),
            "{:20}".format(tournament["name"]),
            "{:20}".format(tournament["location"]),
            "{:20}".format(tournament["nb_rounds"]),
            "{:20}".format(tournament["time"]),
            tournament["description"],
            sep=" | ",
        )

    def display_header_tournament(self):
        print(
            "{:6}".format("ID"),
            "{:20}".format("Nom"),
            "{:20}".format("Lieu"),
            "{:20}".format("Nombre de tours"),
            "{:20}".format("Durée des matchs"),
            "description",
            sep=" | ",
        )
        print()

    def display_list_tournaments(self, list_tournaments):
        """ Display the tournaments of the list_tournaments
        given as parameter """
        self.display_title("Liste des tournois")
        if not list_tournaments:
            print("Il n'y a aucun tournoi enregistré pour le moment\n")
        else:
            self.display_header_tournament()
            for tournament in list_tournaments:
                self.display_tournament(tournament)
            print()

    # ******************************************************************

    # ******************ROUND*******************************************

    def display_list_rounds(self, list_rounds):
        """ Display the rounds of the list_rounds given as parameter """
        self.display_title("Liste des tours")
        if not list_rounds:
            print("Il n'y a aucun tour enregistré pour le moment\n")
        else:
            for round in list_rounds:
                self.display_round(round)
            print()

    def display_round_name(self, round):
        print()
        print("----", round.name.upper(), "----")
        print()

    def display_round(self, round):
        """ Display round's info from the dictionary given as parameter """
        print(
            "{:10}".format(round["name"]),
            "{:.16}".format(round["time_start"]),
            "{:.16}".format(round["time_end"]),
            sep=" | ",
        )

    # ******************************************************************

    # ******************GAME********************************************

    def display_header_games(self):
        print(
            "{:41}".format("Joueur 1"),
            "{:6}".format("ID"),
            "{:6}".format("Score"),
            "{:41}".format("Joueur 2"),
            "{:6}".format("ID"),
            "{:6}".format("Score"),
            sep=" | ",
        )
        print()

    def display_game(self, player_1, player_2, score_1, score_2):
        """ Display game's info with the two players' info
        and their respective scores for that specific game """
        print(
            "{0:20} {1:20}".format(player_1.first_name, player_1.last_name),
            "id={:<3}".format(player_1.doc_id),
            "{:6}".format(score_1),
            "{0:20} {1:20}".format(player_2.first_name, player_2.last_name),
            "id={:<3}".format(player_2.doc_id),
            "{:6}".format(score_2),
            sep=" | ",
        )
