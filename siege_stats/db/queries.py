# Admin Queries
get_admin_by_id = "SELECT * FROM bot_admins WHERE discord_user_id=%s LIMIT 1;"

# Alias Queries
add_alias = "insert into player_aliases(player_id, alias) values(%s, %s);"
get_alias = "SELECT * FROM player_aliases WHERE player_id=%s and alias=%s;"
get_player_aliases = "SELECT alias FROM player_aliases WHERE player_id=%s;"

# Guild Queries
add_guild = "INSERT INTO guilds(guild_id, guild_name) values(%s, %s);"
set_guild_name = "UPDATE guilds SET guild_name=%s WHERE guild_id=%s;"
get_guild_by_name = "SELECT guild_id FROM guilds WHERE guild_name=%s;"
get_guild_name = "SELECT guild_name FROM guilds WHERE guild_id=%s;"

# Permissions Queries
add_guild_permission_for_team = "INSERT INTO bot_permissions(permission_holder_type, permission_object_type, permission_holder, permission_object) values(2, 2, %s, %s);"
get_user_permissison_for_player_id = "SELECT * FROM bot_permissions WHERE permission_holder_type=1 and permission_object_type=1 and permission_holder=%s and permission_object=%s;"
get_guild_permissison_for_player_id = "SELECT * FROM bot_permissions WHERE permission_holder_type=2 and permission_object_type=1 and permission_holder=%s and permission_object=%s;"
get_user_permissison_for_team_id = "SELECT * FROM bot_permissions WHERE permission_holder_type=1 and permission_object_type=2 and permission_holder=%s and permission_object=%s;"
get_guild_permissison_for_team_id = "SELECT * FROM bot_permissions WHERE permission_holder_type=2 and permission_object_type=2 and permission_holder=%s and permission_object=%s;"


# Player Queries
select_player = "SELECT player_id FROM players WHERE player_name=LOWER(%s);"
insert_player = "INSERT INTO players(player_name) values(LOWER(%s)) RETURNING player_id;"

# Map Queries
select_map_id = "SELECT map_id FROM maps WHERE map_name=%s;"

# Match Type Queries
select_match_type_id = "SELECT type_id FROM match_types WHERE type_name=%s;"

# Match Queries
select_match = "SELECT match_id FROM matches WHERE analyst_identifier=%s;"
insert_match = "INSERT INTO matches(analyst_identifier, map_id, match_type_id, rounds_won, rounds_lost, score_at_half, attacker_start, team_id) values(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING match_id;"
get_matches_by_match_type = "SELECT match_id FROM matches WHERE match_type_id=%s;"

# Match Type Queries
get_match_type_id_from_string = "SELECT * FROM match_types WHERE type_name = %s;"

# Team Queries
select_team_from_player = "SELECT team_id FROM teams WHERE player_id=%s;"
select_team_from_name = "SELECT team_id FROM team_names WHERE team_name=%s;"
select_team_name_from_id = "SELECT team_name FROM team_names WHERE team_id=%s;"
insert_team = "INSERT INTO teams(team_id, player_id) values(%s, %s);"
insert_team_name = "INSERT INTO team_names(team_id, team_name) values(%s, %s);"
insert_team_player = "INSERT INTO teams(player_id) values(%s) RETURNING team_id;"
insert_player_into_team = "INSERT INTO teams(team_id, player_id) values(%s, %s);"
update_team_name = "UPDATE team_names SET team_name=%s WHERE team_id=%s;"

# Stats Queries
# WARNING select_stat's order CANNOT BE CHANGED without chaning
# commands.playerstats.py's implementation of creating objects. The ordering is tied directly.
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
select_stat_by_player_and_match = """SELECT 
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
    player_id=%s and match_id=%s;"""
select_stat = "SELECT * FROM stats WHERE stat_id=%s;"
insert_stat = "INSERT INTO stats(player_id, match_id, map_id, rating, attack_rating, defence_rating, kill_differential, entry_differential, trade_differential, kost, kills_per_round, survival_percentage, headshot_percentage, multi_kill_rounds, deaths, kills, defuser_planted, defuser_disabled, team_kills) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING stat_id;"
