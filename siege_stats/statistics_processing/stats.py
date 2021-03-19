class Stats:
    TRANSLATION_DICT = {
        "Player Rating": "rating",
        "ATK Rating": "attackRating",
        "DEF Rating": "defenceRating",
        "K-D (+/-)": "killDifferential",
        "Entry (+/-)": "entryDifferential",
        "Trade Diff.": "tradeDifferential",
        "KOST": "kost",
        "KPR": "killsPerRound",
        "SRV": "survivalPercent",
        "HS%": "headshotPercent",
        "Multikill Rounds": "multiKillRounds",
        "Deaths": "deaths",
        "Kills": "kills",
        "Planted Defuser": "defuserPlanted",
        "Disabled Defuser": "defuserDisabled",
        "Teamkills": "teamKills",
    }

    PARSE_VALUE = {
        "rating": lambda x: float(x),
        "attackRating": lambda x: float(x),
        "defenceRating": lambda x: float(x),
        "killDifferential": lambda x: int("".join(x.split("(")[1][:-1])),
        "entryDifferential": lambda x: int("".join(x.split("(")[1][:-1])),
        "tradeDifferential": lambda x: int(x),
        "kost": lambda x: float(x),
        "killsPerRound": lambda x: float(x),
        "survivalPercent": lambda x: float(x),
        "headshotPercent": lambda x: float("0." + x[:-1]),
        "multiKillRounds": lambda x: int(x),
        "deaths": lambda x: int(x),
        "kills": lambda x: int(x),
        "defuserPlanted": lambda x: int(x),
        "defuserDisabled": lambda x: int(x),
        "teamKills": lambda x: int(x)
    }

    AGGREGATE_VALUES = {
        "rating": lambda x: round(sum(x) / len(x), 3),
        "attackRating": lambda x: round(sum(x) / len(x), 3),
        "defenceRating": lambda x: round(sum(x) / len(x), 3),
        "killDifferential": lambda x: sum(x),
        "entryDifferential": lambda x: sum(x),
        "tradeDifferential": lambda x: sum(x),
        "kost": lambda x: round(sum(x) / len(x), 3),
        "killsPerRound": lambda x: round(sum(x) / len(x), 3),
        "survivalPercent": lambda x: round(sum(x) / len(x), 3),
        "headshotPercent": lambda x: round(sum(x) / len(x), 3),
        "multiKillRounds": lambda x: round(sum(x) / len(x), 3),
        "deaths": lambda x: sum(x),
        "kills": lambda x: sum(x),
        "defuserPlanted": lambda x: round(sum(x) / len(x), 3),
        "defuserDisabled": lambda x: round(sum(x) / len(x), 3),
        "teamKills": lambda x: sum(x)
    }

    OUTPUT_PREFIXES = {
        "rating": "Average",
        "attackRating": "Average",
        "defenceRating": "Average",
        "killDifferential": "Total",
        "entryDifferential": "Total",
        "tradeDifferential": "Total",
        "kost": "Average",
        "killsPerRound": "Average",
        "survivalPercent": "Average",
        "headshotPercent": "Average",
        "multiKillRounds": "Average",
        "deaths": "Total",
        "kills": "Total",
        "defuserPlanted": "Average",
        "defuserDisabled": "Average",
        "teamKills": "Total"
    }

    FIELD_TO_STRING = {
        "rating": "rating",
        "attackRating": "attack rating",
        "defenceRating": "defence rating",
        "killDifferential": "kill differential",
        "entryDifferential": "entry differential",
        "tradeDifferential": "trade differential",
        "kost": "KOST",
        "killsPerRound": "kills per round",
        "survivalPercent": "chance to survive round",
        "headshotPercent": "headshot percentage",
        "multiKillRounds": "multi-kill rounds per game",
        "deaths": "deaths",
        "kills": "kills",
        "defuserPlanted": "defusers planted per game",
        "defuserDisabled": "defusers disabled per game",
        "teamKills": "team kills"
    }

    def __init__(self):
        self.rating = []
        self.attackRating = []
        self.defenceRating = []
        self.killDifferential = []
        self.entryDifferential = []
        self.tradeDifferential = []
        self.kost = []
        self.killsPerRound = []
        self.survivalPercent = []
        self.headshotPercent = []
        self.multiKillRounds = []
        self.deaths = []
        self.kills = []
        self.defuserPlanted = []
        self.defuserDisabled = []
        self.teamKills = []

    def get_rating(self):
        return self.AGGREGATE_VALUES["rating"](self.rating)

    def get_attack_rating(self):
        return self.AGGREGATE_VALUES["attackRating"](self.attackRating)

    def get_defence_rating(self):
        return self.AGGREGATE_VALUES["defenceRating"](self.defenceRating)

    def get_kill_differential(self):
        return self.AGGREGATE_VALUES["killDifferential"](self.killDifferential)

    def get_entry_differential(self):
        return self.AGGREGATE_VALUES["entryDifferential"](self.entryDifferential)

    def get_trade_differential(self):
        return self.AGGREGATE_VALUES["tradeDifferential"](self.tradeDifferential)

    def get_kost(self):
        return self.AGGREGATE_VALUES["kost"](self.kost)

    def get_kills_per_round(self):
        return self.AGGREGATE_VALUES["killsPerRound"](self.killsPerRound)

    def get_survival_percent(self):
        return self.AGGREGATE_VALUES["survivalPercent"](self.survivalPercent)

    def get_headshot_percent(self):
        return self.AGGREGATE_VALUES["headshotPercent"](self.headshotPercent)

    def get_multi_kill_rounds(self):
        return self.AGGREGATE_VALUES["multiKillRounds"](self.multiKillRounds)

    def get_deaths(self):
        return self.AGGREGATE_VALUES["deaths"](self.deaths)

    def get_kills(self):
        return self.AGGREGATE_VALUES["kills"](self.kills)

    def get_defuser_planted(self):
        return self.AGGREGATE_VALUES["defuserPlanted"](self.defuserPlanted)

    def get_defuser_disabled(self):
        return self.AGGREGATE_VALUES["defuserDisabled"](self.defuserDisabled)

    def get_team_kills(self):
        return self.AGGREGATE_VALUES["teamKills"](self.teamKills)    

    def add_data_point(self, raw_name, raw_value):
        actual_name = self.TRANSLATION_DICT[raw_name]
        actual_value = self.PARSE_VALUE[actual_name](raw_value)

        getattr(self, actual_name).append(actual_value)

    def __add__(self, other):
        for field in self.TRANSLATION_DICT.values():
            setattr(self, field, getattr(self, field) + getattr(other, field))

        return self

    def __str__(self):
        stat_string = "Statistics:\n"
        for field in self.TRANSLATION_DICT.values():
            stat_string += f">\t{self.OUTPUT_PREFIXES[field]} {self.FIELD_TO_STRING[field]}: {self.AGGREGATE_VALUES[field](getattr(self, field))}\n"

        return stat_string

class StatsParser:

    """ Parses out an individual file (as defined by it's header and data)'s stats """
    def __init__(self, header, team_data):
        self.header = header
        self.team_data = team_data

    def get_header_position(self, string):
        return self.header.split(",").index(string)

    def parse_players(self):
        return [data_line.split(",")[self.get_header_position("Player")] for data_line in self.team_data]

    def parse_stat(self, stat_name):
        player_stat = {}
        for data_line in self.team_data:
            data = data_line.split(",")
            player = data[self.get_header_position("Player")]
            data_point = data[self.get_header_position(stat_name)]

            player_stat[player] = (stat_name, data_point)

        return [(player, player_stat[player]) for player in player_stat.keys()]

    def parse_stats(self):
        """ Parses out keys stats from the initialized data

        Returns: Stats object with this file's data.
        """
        player_data = {}

        # Parse out raw strings from the data line.
        for data_name in Stats.TRANSLATION_DICT.keys():
            for player, data_point in self.parse_stat(data_name):
                if player in player_data:
                    player_data[player].append(data_point)
                else:
                    player_data[player] = [data_point]

        # Get a new empty dicionary where each player has an empty stats object.
        player_stats = {player: Stats() for player in player_data.keys()}

        # Feed each stat to the Stats object.
        for player in player_data.keys():
            for data_point in player_data[player]:
                player_stats[player].add_data_point(*data_point)

        return [(player, player_stats[player]) for player in player_stats.keys()]
