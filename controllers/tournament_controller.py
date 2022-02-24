import datetime

from views.main_view import Display
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from .player_controller import PlayerController


class TournamentController:
    def __init__(self, home):
        self.display = Display()
        self.home = home
        self.playerController = PlayerController(home)

    def get_info_tournaments(self):
        """ Display tournaments and tournament info choice menu
        and does the right action according to user choice """
        self.display_tournaments()

        menu = {"1": "Voir les infos d'un tournoi"}
        response = self.display.display_menu(menu)

        if response == "1":
            tournament = self.select_tournament_by_id()
            self.choose_info_tournament(tournament)
        elif response == "h":
            self.home()

        self.get_info_tournaments()

    def select_tournament_by_id(self):
        """ Returns a Tournament's instance
        accordind to id's choice of user """
        id = self.display.verified_response(
            "Veuillez entrer l'id du tournoi: ", r"^\d+$"
        )
        tournament = Tournament.get_tournament_by_id(int(id))
        if not tournament:
            self.display.display_message("Tournoi non trouvé, recommencez")

            return self.select_tournament_by_id()

        return Tournament(**tournament, doc_id=int(id))

    def choose_info_tournament(self, tournament):
        """ Display tournament info menu
        and does the right action according to user choice """
        menu = {
            "1": "Voir les joueurs du tournoi",
            "2": "Voir les tours du tournoi",
            "3": "Voir les matchs du tournoi",
        }
        response = self.display.display_menu(menu)

        if response == "1":
            self.get_list_players_tournament(tournament)
        if response == "2":
            self.get_list_rounds_tournament(tournament.list_rounds)
        if response == "3":
            self.get_list_games_tournament(tournament.list_rounds)
        elif response == "h":
            self.home()

        self.choose_info_tournament(tournament)

    def get_list_players_tournament(self, tournament):
        """ Returns all the players of a tournament """
        list_players = []
        for id in tournament.list_players:
            list_players.append(Player.get_player_by_id(id))
        self.display.display_list_players(list_players)

    def get_list_rounds_tournament(self, list_rounds):
        """ Returns all the rounds of a tournament """
        self.display.display_list_rounds(list_rounds)

    def get_players_objects(self, id_1, id_2):
        """ Returns two Player's instances
        according to the object's player given in parameters """
        player_1 = Player.get_player_by_id(id_1)
        player_1 = Player(**player_1, doc_id=id_1)
        player_2 = Player.get_player_by_id(id_2)
        player_2 = Player(**player_2, doc_id=id_2)

        return player_1, player_2

    def get_list_games_tournament(self, list_rounds):
        """ Display all the games of a tournament """
        if list_rounds == []:
            self.display.display_message(
                "Il n'y a aucun match à afficher pour le moment"
            )
        else:
            self.display.display_header_games()
            for round in list_rounds:
                for game in round["list_games"]:
                    # game representation : [[id_1, score_1], [id_2, score_2]]
                    id_1 = game[0][0]
                    id_2 = game[1][0]
                    player_1, player_2 = self.get_players_objects(id_1, id_2)
                    score_1 = game[0][1]
                    score_2 = game[1][1]
                    self.display.display_game(
                        player_1,
                        player_2,
                        score_1,
                        score_2
                    )

    def display_tournaments(self):
        """ Display all the tournaments from database """
        list_tournaments = Tournament.get_all_tournaments()
        self.display.display_list_tournaments(list_tournaments)

    def launch_tournament(self):
        """ Display tournament management menu
        and does the right action according to user choice """
        self.display.display_title("Gestion des tournois")
        menu = {"1": "Créer un tournoi", "2": "Charger un tournoi"}
        response = self.display.display_menu(menu)

        if response == "1":
            self.create_tournament()
        if response == "2":
            self.display_tournaments()
            self.load_tournament()
        elif response == "h":
            self.home()

        self.launch_tournament()

    def create_tournament(self):
        """ Create a new tournament with all info given by user
        and this new tournament in database """
        self.display.display_title("Création d'un tournoi")

        name = input("Veuillez entrer le nom: ")
        location = input("Veuillez entrer le lieu: ")
        nb_rounds = self.display.verified_response(
            "Veuillez entrer le nombre de tours: ", r"^\d+$"
        )
        time = self.display.verified_response(
            "Veuillez entrer le temps de jeu: 1 bullet - 2 blitz - 3 rapide ",
            "^(1|2|3)$",
        )
        if time == 1:
            time = "bullet"
        elif time == 2:
            time = "blitz"
        elif time == 3:
            time = "rapide"
        description = input("Veuillez entrer une description: ")
        list_rounds = []
        list_players = []

        tournament = Tournament(
            name,
            location,
            list_rounds,
            list_players,
            time,
            description,
            nb_rounds
        )
        tournament.save()

    def load_tournament(self):
        """ Allows to choose a tournament and load it if it's not over """
        self.display.display_title("Chargement d'un tournoi")
        tournament = self.select_tournament_by_id()

        if len(tournament.list_players) < 8:
            tournament = self.add_players(tournament)
        else:
            if tournament.is_over == 1:
                self.display.display_title("Tournoi terminé !")
            else:
                self.display.display_title("Lancement du tournoi !")
                tournament = self.play_tournament(tournament)

    def add_players(self, tournament):
        """ Returns tournament
        with new players added in tournament.list_players """
        self.display.display_message(
            "\nPour commencer le tournoi veuillez ajouter des joueurs"
        )
        while len(tournament.list_players) < 8:
            player = self.playerController.choose_player()
            if player:
                if player.doc_id in tournament.list_players:
                    self.display.display_message(
                        "Ce joueur a déjà été ajouté au tournoi"
                    )
                else:
                    tournament.list_players.append(player.doc_id)
                    tournament.save()

        return tournament

    # ******************PLAY TOURNAMENT*********************************

    def sort_round(self, list_players, sort_type):
        """
        Returns players sorted according to sort_type

            Parameters:
                list_players (int[]): a list of id's players
                sort_type (str): a string to determine the sort type

            Returns:
                list of Player's instances sorted
        """
        list_players_for_round = []
        for id in list_players:
            player = Player.get_player_by_id(int(id))
            player = Player(**player, doc_id=int(id))
            if player:
                list_players_for_round.append(player)
        if sort_type == "rank":
            return sorted(
                list_players_for_round,
                key=lambda i: (i.rank, i.doc_id),
                reverse=True
            )
        else:
            return sorted(
                list_players_for_round,
                key=lambda i: (i.score, i.rank),
                reverse=True
            )

    def start_round_prompt(self):
        """ Returns response of starting a new round """
        return self.display.verified_response(
            "Voulez-vous démarrer un tour ?"
            " 1: oui, je lance un nouveau tour - 2: non, retour au menu ",
            "^(1|2)$",
        )

    def end_round_prompt(self):
        """ Returns response of ending current round """
        return self.display.verified_response(
            "Tapez 1 pour marquer le tour comme terminé: ",
            "^(1)$"
        )

    def handle_round(self, tournament):
        """ Returns tournament if a round has been played,
        this tournament will contain a new round in list_rounds """
        if self.start_round_prompt() == "2":
            self.launch_tournament()
        else:
            tournament = self.play_round(tournament)

        return tournament

    def display_games(self, list_games):
        """ Display all the games that have to be played in current round """
        self.display.display_title("Liste des matchs")
        for game in list_games:
            # game representation : [[id_1, score_1], [id_2, score_2]]
            player_1, player_2 = self.get_players_objects(
                game[0][0],
                game[1][0]
            )

            self.display.display_pairs_players(player_1, player_2)

    def handle_update_score(self, player, new_score):
        """
        Returns new_score of a player and save new player.score

            Parameters:
                player (Player): Player's instance
                new_score (int): score of the player for this game

            Returns:
                new_score (int) : score of the player for this game
        """
        self.display.display_player_for_score(player)
        response = self.display.verified_response("", "^(0|1|0.5)$")
        if response:
            new_score += float(response)
            player.score += new_score

        player.save()

        return new_score

    def fill_scores(self, list_games):
        """ Returns the list of games updated with players' scores """
        for game in list_games:
            # game representation : [[id_1, score_1], [id_2, score_2]]
            player_1, player_2 = self.get_players_objects(
                game[0][0],
                game[1][0]
            )

            game[0][1] = self.handle_update_score(player_1, game[0][1])
            game[1][1] = self.handle_update_score(player_2, game[1][1])

        return list_games

    def manage_end_round(
        self,
        name,
        time_start,
        is_over,
        list_games,
        tournament
    ):
        """
        Returns tournament updated
        with new round added to list_round

            Parameters:
                name (str): round's name
                time_start (str): round's starting time
                is_over (int): round's attribute to know if round is over
                list_games (list[[[int, int]]]): round's games
                tournament (Tournament): current tournament

            Returns:
                tournament (Tournament) : tournament updated
        """
        if is_over:
            time_end = str(datetime.datetime.today())
            self.display.display_message(
                "Fin du tour, veuillez rentrer les scores des joueurs: "
            )
            list_games = self.fill_scores(list_games)

        round = Round(name, list_games, time_start, time_end, is_over)
        tournament.list_rounds.append(Round.get_serialized_round(round))
        tournament.save()

        return tournament

    def update_rank_players(self, list_players):
        """ Allows to update ranks of all the players from a tournament """
        self.display.display_message("Mise à jour des scores")
        for id in list_players:
            player = Player.get_player_by_id(id)
            player = Player(**player, doc_id=id)
            self.display.display_player_object(player)
            rank = self.display.verified_response(
                "Veuillez entrer le nouveau classement "
                "(score compris entre 100 et 9999: ",
                r"^\d{3,4}$",
            )
            player.rank = rank
            player.save()

    def reset_score_players(self, list_rounds, nb_rounds, list_players):
        """
        Reset the scores of players if all rounds have been played

            Parameters:
                list_rounds (list[Round]): tournament's rounds
                nb_rounds (str): tournament's number of rounds
                list_players (list[int]): tournament's players
        """
        if len(list_rounds) == int(nb_rounds):
            for id in list_players:
                player = Player.get_player_by_id(id)
                player = Player(**player, doc_id=id)
                player.score = 0
                player.save()

    def manage_end_tournament(self, tournament):
        """ Returns tournament updated as over
        after player's scores reset and their ranks updated """
        self.reset_score_players(
            tournament.list_rounds,
            tournament.nb_rounds,
            tournament.list_players
        )
        self.update_rank_players(tournament.list_players)
        tournament.is_over = 1
        tournament.save()
        self.display.display_title("Tournoi terminé !")

        return tournament

    def play_round(self, tournament):
        """ Returns tournament after playing one round """
        nb_rounds_done = len(tournament.list_rounds)
        list_players = self.sort_round(
            tournament.list_players,
            "rank" if nb_rounds_done == 0 else "score"
        )

        self.display.display_message("Début du tour")
        list_games = self.get_list_games(
                list_players,
                tournament.list_rounds
        )
        self.display_games(list_games)

        return self.manage_end_round(
            "Round " + str(nb_rounds_done + 1),
            str(datetime.datetime.today()),
            self.end_round_prompt(),
            list_games,
            tournament
        )

    def play_tournament(self, tournament):
        """ Returns tournament after playing [tournament.nb_rounds] rounds """
        while len(tournament.list_rounds) < int(tournament.nb_rounds):
            tournament = self.handle_round(tournament)

        return self.manage_end_tournament(tournament)

    # ******************PAIRING PLAYERS*******************************

    def get_list_all_pairs(self, list_rounds):
        """ Returns all pairs of players
        that were played during the tournament """
        list_pairs = []
        for round in list_rounds:
            for game in round["list_games"]:
                # game representation : [[id_1, score_1], [id_2, score_2]]
                player_1 = game[0][0]
                player_2 = game[1][0]
                list_pairs.append((player_1, player_2))

        return list_pairs

    def get_list_games_first_round(self, list_players):
        """ Returns the games to play for the first round -
        the players are "mixed" according to their rank """
        half = len(list_players) // 2
        list_sup = list_players[:half]
        list_inf = list_players[half:]
        list_games = []

        for i in range(len(list_players) // 2):
            player_1 = list_sup[i]
            player_2 = list_inf[i]
            list_games.append(([player_1.doc_id, 0], [player_2.doc_id, 0]))
            i = i + 1

        return list_games

    def get_list_games(self, list_players, list_rounds):
        """ Returns the games to play weither it's first or other rounds """
        list_games = []
        list_all_pairs = self.get_list_all_pairs(list_rounds)

        if list_rounds == []:
            list_games = self.get_list_games_first_round(list_players)
        else:
            self.get_list_games_next_rounds(
                list_games,
                list_players,
                list_all_pairs
            )

        return list_games

    def copy_list(self, dest, src):
        for i in range(len(dest)):
            dest.pop()
        for i in range(len(src)):
            dest.append(src[i])

    def get_list_games_next_rounds(
        self, list_games, list_players, list_all_pairs
    ):
        """
        Fill list_games with games to play where
        players are paired according to swiss system

            Parameters:
                list_games (list[[[int, int]]]): round's games
                list_players (list): players sorted by their scores
                list_all_pairs (list[(int, int)]): all players' paired
                in all previous games

            Returns:
                bool: Weither the pair is valid or not
        """
        list_games_copy = list_games.copy()
        list_players_copy = list_players.copy()
        ret = False
        i = 1

        while i < len(list_players):
            player_1 = list_players[0]
            player_2 = list_players[i]
            pair = (player_1.doc_id, player_2.doc_id)

            if len(list_players) == 2 and pair not in list_all_pairs:
                list_games.append(([player_1.doc_id, 0], [player_2.doc_id, 0]))

                return True

            if pair not in list_all_pairs:
                list_games.append(([player_1.doc_id, 0], [player_2.doc_id, 0]))
                list_players.remove(player_1)
                list_players.remove(player_2)
                ret = self.get_list_games_next_rounds(
                    list_games,
                    list_players,
                    list_all_pairs
                )
            if ret:
                return True

            self.copy_list(list_games, list_games_copy)
            self.copy_list(list_players, list_players_copy)
            i += 1

        return False
