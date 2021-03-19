
# Player Queries
select_player = "SELECT player_id FROM players WHERE player_name=%s;"
insert_player = "INSERT INTO players(player_name) values(%s) RETURNING player_id;"

# Map Queries
select_map_id = "SELECT map_id FROM maps WHERE map_name=%s;"

# Match Type Queries
select_match_type_id = "SELECT type_id FROM match_types WHERE type_name=%s;"

# Match Queries
select_match = "SELECT match_id FROM matches WHERE analyst_identifier=%s;"
insert_match = "INSERT INTO matches(analyst_identifier, map_id, match_type_id, rounds_won, rounds_lost, score_at_half, attacker_start) values(%s, %s, %s, %s, %s, %s, %s) RETURNING match_id;"

# Stats Queries
select_stat = "SELECT * FROM stats WHERE stat_id=%s;"
insert_stat = "INSERT INTO stats(player_id, match_id, map_id, rating, attack_rating, defence_rating, kill_differential, entry_differential, trade_differential, kost, kills_per_round, survival_percentage, headshot_percentage, multi_kill_rounds, deaths, kills, defuser_planted, defuser_disabled, team_kills) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING stat_id;"