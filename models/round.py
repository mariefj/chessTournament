class Round:
    def __init__(self, name, list_games, time_start, time_end, is_over):
        """
        Constructs Round's instance

            Parameters:
                name (str): round's name - "Round [int]"
                list_games (list[[[int, int]]]): round's games
                time_start (str): round's time_start
                time_end (str): round's time_end
                is_over (int): 0 round is playing - 1 round over
        """
        self.name = name
        self.list_games = list_games
        self.time_start = time_start
        self.time_end = time_end
        self.is_over = is_over

    def get_serialized_round(self):
        """ Returns a dictionary with the round info """
        return {
            "name": self.name,
            "list_games": self.list_games,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "is_over": self.is_over,
        }
