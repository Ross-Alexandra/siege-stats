
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
# WARNING select_stat's order CANNOT BE CHANGED without chaning
# bot.py's implementation of creating objects. The ordering is tied directly.
select_stat_by_player = """SELECT 
    rating,
    attack_rating,
    defence_rating,
    kill_differential,
    entry_differential,
    trade_differential,
    kost,
    kills_per_round,
    survival_percentage,
    headshot_percentage,
    multi_kill_rounds,
    deaths,
    kills,
    defuser_planted,
    defuser_disabled,
    team_kills
FROM 
    stats 
WHERE
    player_id=%s;"""
select_stat = "SELECT * FROM stats WHERE stat_id=%s"
insert_stat = "INSERT INTO stats(player_id, match_id, map_id, rating, attack_rating, defence_rating, kill_differential, entry_differential, trade_differential, kost, kills_per_round, survival_percentage, headshot_percentage, multi_kill_rounds, deaths, kills, defuser_planted, defuser_disabled, team_kills) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING stat_id;"

# Team Queries
select_team_from_player = "SELECT team_id FROM teams WHERE player_id=%s;"
insert_team_player = "INSERT INTO teams(player_id) values(%s) RETURNING team_id;"
insert_team = "INSERT INTO teams(team_id, player_id) values(%s, %s);"

# Map Win/Loss Query
select_map_win_loss = """with mapWinLoss
as (
	select 
		rounds_won > rounds_lost as match_won,
		map_name
	from 
		matches natural join maps
),
mapWins as (
	select 
		map_name,
		count(map_name) as map_wins
	from
		mapWinLoss
	where
		match_won = true
	group by map_name
),
mapLosses as (
	select 
		map_name,
		count(map_name) as map_losses
	from
		mapWinLoss
	where
		match_won = false
	group by map_name
)
select 
	map_name,
	coalesce (mapWins.map_wins, 0) as wins,
	coalesce (mapLosses.map_losses, 0) as losses
from 
	mapWins full join mapLosses using (map_name);"""