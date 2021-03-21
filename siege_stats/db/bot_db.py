import siege_stats.db.db_settings as db_settings
import siege_stats.db.queries as queries

import psycopg2


class BotDB:
    def __init__(self):
        self._connection = psycopg2.connect(
            host=db_settings.host,
            database=db_settings.database,
            user=db_settings.db_user,
            password=db_settings.db_pass,
            port=db_settings.port
        )

    def _get_player_id(self, player_name):
        curs = self._connection.cursor()
        curs.execute(queries.select_player, (player_name,))

        player_id = curs.fetchall()

        return None if len(player_id) == 0 else player_id[0]

    def _add_player(self, player_name):
        curs = self._connection.cursor()
        curs.execute(queries.select_player, (player_name,))

        player_id = curs.fetchone()

        # Check if the player already exists in the database.
        if player_id:
            print("Name already present.")
            curs.close()

            return player_id[0], False

        curs.execute(queries.insert_player, (player_name,))
        player_id = curs.fetchone()[0]

        curs.close()
        self._connection.commit()

        return player_id, True

    def _get_map_id(self, map_name):
        curs = self._connection.cursor()
        curs.execute(queries.select_map_id, (map_name,))

        # Fetch the map_id from the database.
        map_id = curs.fetchone()
        if map_id is None:
            curs.execute(queries.select_map_id, ("UNKNOWN",))
            map_id = curs.fetchone()

        curs.close()
        self._connection.commit()

        return map_id[0]

    def _get_match_type_id(self, match_type):
        curs = self._connection.cursor()
        curs.execute(queries.select_match_type_id, (match_type,))

        match_type_id = curs.fetchone()
        if match_type_id is None:
            curs.execute(queries.select_match_type_id, ("scrim",))
            match_type_id = curs.fetchone()

        curs.close()
        self._connection.commit()

        return match_type_id[0]

    def add_team(self, players):
        curs = self._connection.cursor()
        team_sets = []
        player_ids = []

        # Iterate through each player and get a set
        # of the teams they play on, and a list of player_ids.
        for player in players:
            player_id, _ = self._add_player(player)
            player_ids.append(player_id)

            curs.execute(queries.select_team_from_player, (player_id,))
            team_sets.append({value[0] for value in curs.fetchall()})
        
        # Intersect all the sets together, if there's any
        # values left, then all players are on that team.
        team_ids = team_sets[0]
        for team_set in team_sets[1:]:
            team_ids = team_ids.intersection(team_set)

        # If there are any team_ids remaining, then 
        # this is not a new team.
        if team_ids:

            curs.close()
            self._connection.commit()
            return team_ids.pop(), False

        # Otherwise this is a new team, so insert a player, get a team
        # id back, and insert the rest of the teams based off that 
        # id.
        curs.execute(queries.insert_team_player, (player_ids[0],))
        team_id = curs.fetchone()[0]
        for player_id in player_ids[1:]:
            curs.execute(queries.insert_team, (team_id, player_id))

        curs.close()
        self._connection.commit()
        return team_id, True
    
    def add_match(self, analyst_identifier: str, map_str: str, match_type: str, rounds_won: int, rounds_lost: int, score_at_half: int, attackers_start: bool, team_id: int):

        map_id = self._get_map_id(map_str)
        match_type_id = self._get_match_type_id(match_type)

        curs = self._connection.cursor()
        curs.execute(queries.select_match, (analyst_identifier,))
        match_id = curs.fetchone()

        if match_id:
            print("Match already present.")
            return match_id[0], False

        curs.execute(queries.insert_match, (analyst_identifier, map_id, match_type_id, rounds_won, rounds_lost, score_at_half, attackers_start, team_id))
        match_id = curs.fetchone()[0]

        curs.close()
        self._connection.commit()

        return match_id, True

    def add_statistic(self, player: str,
                             match_id: int, 
                             map_string: str,
                             rating: float,
                             attack_rating: float,
                             defence_rating: float,
                             kill_differential: int,
                             entry_differential: int,
                             trade_differential: int,
                             kost: float,
                             kills_per_round: float,
                             survival_percentage: float,
                             headshot_percentage: float,
                             multi_kill_rounds: int,
                             deaths: int,
                             kills: int,
                             defuser_planted: int,
                             defuser_disabled: int,
                             team_kills: int):
                             
        map_id = self._get_map_id(map_string)
        player_id, _ = self._add_player(player)

        curs = self._connection.cursor()

        # Assume if we're running this then we know that this is a unique stat.
        curs.execute(queries.insert_stat, (player_id, match_id, map_id, rating, attack_rating, defence_rating, kill_differential, entry_differential, trade_differential, kost, kills_per_round, survival_percentage, headshot_percentage, multi_kill_rounds, deaths, kills, defuser_planted, defuser_disabled, team_kills))
        stats_id = curs.fetchone()[0]

        curs.close()
        self._connection.commit()

        return stats_id

    def get_player_stats(self, player_name):
        curs = self._connection.cursor()
        player_id = self._get_player_id(player_name)

        if player_id is None:
            return []

        curs.execute(queries.select_stat_by_player, (player_id,))
        player_stats = curs.fetchall()

        curs.close()
        return player_stats

    def close(self):
        self._connection.close()