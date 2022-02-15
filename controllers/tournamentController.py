import datetime

from views.mainView import Display
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from .playerController import PlayerController


class TournamentController:
    def __init__(self, home):
        self.display = Display()
        self.home = home
        self.playerController = PlayerController(home)

    def get_info_tournaments(self):
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
        id = self.display.verified_response(
            "Veuillez entrer l'id du tournoi: ", r"^\d+$"
        )
        tournament = Tournament.get_tournament_by_id(int(id))
        if not tournament:
            self.display.display_message("Tournoi non trouvé, recommencez")

            return self.select_tournament_by_id()

        return Tournament(**tournament, doc_id=int(id))

    def choose_info_tournament(self, tournament):
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
        list_players = []
        for id in tournament.list_players:
            list_players.append(Player.get_player_by_id(id))
        self.display.display_list_players(list_players)

    def get_list_rounds_tournament(self, list_rounds):
        self.display.display_list_rounds(list_rounds)

    def get_players_objects(self, id_1, id_2):
        player_1 = Player.get_player_by_id(id_1)
        player_1 = Player(**player_1, doc_id=id_1)
        player_2 = Player.get_player_by_id(id_2)
        player_2 = Player(**player_2, doc_id=id_2)

        return player_1, player_2

    def get_list_games_tournament(self, list_rounds):
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
        list_tournaments = Tournament.get_all_tournaments()
        self.display.display_list_tournaments(list_tournaments)

    def launch_tournament(self):
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
        return self.display.verified_response(
            "Voulez-vous démarrer un tour ?"
            " 1: oui, je lance un nouveau tour - 2: non, retour au menu ",
            "^(1|2)$",
        )

    def end_round_prompt(self):
        return self.display.verified_response(
            "Tapez 1 pour marquer le tour comme terminé: ",
            "^(1)$"
        )

    def handle_round(self, tournament):
        if self.start_round_prompt() == "2":
            self.launch_tournament()
        else:
            tournament = self.play_round(tournament)

        return tournament

    def display_games(self, list_games):
        self.display.display_title("Liste des matchs")
        for game in list_games:
            # game representation : [[id_1, score_1], [id_2, score_2]]
            player_1, player_2 = self.get_players_objects(
                game[0][0],
                game[1][0]
            )

            self.display.display_pairs_players(player_1, player_2)

    def handle_update_score(self, player, new_score):
        self.display.display_player_for_score(player)
        response = self.display.verified_response("", "^(0|1|0.5)$")
        if response:
            new_score += float(response)
            player.score += new_score

        player.save()

        return new_score

    def fill_scores(self, list_games):
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
        if len(list_rounds) == int(nb_rounds):
            for id in list_players:
                player = Player.get_player_by_id(id)
                player = Player(**player, doc_id=id)
                player.score = 0
                player.save()

    def manage_end_tournament(self, tournament):
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
            "Round" + str(nb_rounds_done + 1),
            str(datetime.datetime.today()),
            self.end_round_prompt(),
            list_games,
            tournament
        )

    def play_tournament(self, tournament):
        while len(tournament.list_rounds) < int(tournament.nb_rounds):
            tournament = self.handle_round(tournament)

        return self.manage_end_tournament(tournament)

    # ******************PAIRING PLAYERS*******************************

    def get_list_all_pairs(self, list_rounds):
        list_pairs = []
        for round in list_rounds:
            for game in round["list_games"]:
                # game representation : [[id_1, score_1], [id_2, score_2]]
                player_1 = game[0][0]
                player_2 = game[1][0]
                list_pairs.append((player_1, player_2))

        return list_pairs

    def get_list_games_first_round(self, list_players):
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
