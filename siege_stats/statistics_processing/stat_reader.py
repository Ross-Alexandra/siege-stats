from siege_stats.statistics_processing.stats import Stats, StatsParser

class StatReader:
    """ Reads the stats of multiple files, aggregating the results found """

    _OVERVIEW_DATA_DICT = {
        "Match ID": "matchId",
        "Map": "mapString",
        "Team 1": "teamColor",
        "Team 1 Score": "roundsWon",
        "Team 2 Score": "roundsLost",
        "ATK at Start": "attackStartTeam",
        "Team 1 Score at Half": "scoreAtHalf",
    }

    _OVERVIEW_DATA_CONVERSION = {
        "Match ID": str,
        "Map": str,
        "Team 1": str,
        "Team 1 Score": int,
        "Team 2 Score": int,
        "ATK at Start": str,
        "Team 1 Score at Half": int,
    }

    def __init__(self):
        self.match_data = {}
        self.player_stats = {}

    def _parse_out(self, file, start_string):
        data_strings = []
        
        # Try to find the start_string, if it is not found, empty contents.
        found = False
        for line in file:
            if line.strip() == start_string:
                found = True
                break
        
        if not found:
            print(f"Unable to locate start_string ({start_string}) in the file.")
            return "", []

        try:
            # Setup the line variable, and ignore the header.
            header = file.readline().strip()
        except Exception:
            
            # This is likely unrecoverable, but realistically we were only
            # unable to read the header row, so set it blank and keep trying.
            print("Failed to find header line")
            header = ""

        # For the remaining lines, assume that encountering a "-" means
        # that we have hit the end of the player performance section and move on.
        # If "-" is not encountered, assume the rest of the file is player performance.
        for line in file:
            if line.strip() == "-":
                break
            
            data_strings.append(line.strip())

        file.seek(0) # Reset the fp to 0.
        return header, data_strings

    def collect_match_performance(self, file):
        
        # Attempt to read the file object to parse out the header and
        # 10 performance strings (1 for each player.)
        header, performance_strings = self._parse_out(file, ",MATCH PERFORMANCE")
        
        # If data cannot be parsed from the file object then give up
        if not header or not performance_strings:
            return

        # Otherwise, assume data was parsed correctly and grab
        # the first 5 performance rows (ie, our player's rows.)
        team_data = performance_strings[0:5]
        statsParser = StatsParser(header, team_data)

        # Parse out and register any new players.
        for player in statsParser.parse_players():
            self.register_player(player)

        # Parse out the player's stats from the game.
        for player, stat in statsParser.parse_stats():
            self.player_stats[player] += stat

    def collect_match_overview(self, file):

        # Attempt to read the file object to parse out the header and
        # the match overview.
        header, overview_string = self._parse_out(file, ",MATCH OVERVIEW")
        headerToPosition = lambda x: header.split(",").index(x)

        if not header or not overview_string:
            return

        # Otherwise, assume the data was parsed correctly and grab the
        # required fields. overview_string will only be one string here,
        # so grab that string and split along commas. Ignore the first value
        # as it is empty.
        overview_data = overview_string[0].split(",")
        raw_data_dict = {}
        for data_string in self._OVERVIEW_DATA_DICT.keys():
            index = headerToPosition(data_string)
            raw_data_dict[self._OVERVIEW_DATA_DICT[data_string]] = self._OVERVIEW_DATA_CONVERSION[data_string](overview_data[index])

        self.match_data["matchId"] = f"{raw_data_dict['matchId'].lower()}_{raw_data_dict['teamColor'].lower()}"
        self.match_data["mapString"] = raw_data_dict["mapString"]
        self.match_data["start_attack"] = raw_data_dict["teamColor"] == raw_data_dict["attackStartTeam"]
        self.match_data["roundsWon"] = raw_data_dict["roundsWon"]
        self.match_data["roundsLost"] = raw_data_dict["roundsLost"]
        self.match_data["scoreAtHalf"] = raw_data_dict["scoreAtHalf"]

    def register_player(self, player_name):
        if player_name not in self.player_stats:
            self.player_stats[player_name] = Stats()

    def __add__(self, other):
        for player in self.player_stats.keys():
            if player in other.player_stats:
                self.player_stats[player] += other.player_stats[player]
        
        for player in other.player_stats.keys():
            if player not in self.player_stats:
                self.player_stats[player] = other.player_stats[player]
        
        return self

    def __str__(self):
        reader_string = ""
        for player, stats_obj in self.player_stats.items():
            reader_string += f"{player} {stats_obj}\n"
        
        return reader_string