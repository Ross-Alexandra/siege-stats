CREATE TABLE players (
    player_id serial PRIMARY KEY,
    player_name VARCHAR(20) NOT NULL
);

CREATE TABLE maps (
    map_id serial PRIMARY KEY,
    map_name VARCHAR(20) NOT NULL
);

CREATE TABLE match_types (
    type_id serial PRIMARY KEY,
    type_name VARCHAR(10)
);

CREATE TABLE matches (
    match_id serial PRIMARY KEY,
    analyst_identifier VARCHAR(40),
    map_id serial,
    match_type_id serial,
    rounds_won integer,
    rounds_lost integer,
    score_at_half integer,
    attacker_start boolean,
    CONSTRAINT matches_map_exists FOREIGN KEY(map_id) REFERENCES maps(map_id)
    CONSTRAINT matches_match_type_exists FOREIGN KEY(match_type_id) REFERENCES match_types(type_id)
    CONSTRAINT analyst_identifier_is_unique UNIQUE(analyst_identifier)
);

CREATE TABLE stats (
    stat_id serial PRIMARY KEY,
    player_id serial,
    match_id serial,
    map_id serial,
    rating real,
    attack_rating real,
    defence_rating real,
    kill_differential integer,
    entry_differential integer,
    trade_differential integer,
    kost real,
    kills_per_round real,
    survival_percentage real,
    headshot_percentage real,
    multi_kill_rounds integer,
    deaths integer,
    kills integer,
    defuser_planted integer,
    defuser_disabled integer,
    team_kills integer,
    CONSTRAINT player_exists FOREIGN KEY(player_id) REFERENCES players(player_id),
    CONSTRAINT stat_match_exists FOREIGN KEY(match_id) REFERENCES matches(match_id),
    CONSTRAINT map_exists FOREIGN KEY(map_id) REFERENCES maps(map_id)
);

insert into maps(map_name) values('Villa');
insert into maps(map_name) values('Club House');
insert into maps(map_name) values('Theme Park');
insert into maps(map_name) values('Consulate');
insert into maps(map_name) values('Coastline');
insert into maps(map_name) values('Kafe');
insert into maps(map_name) values('Chalet');
insert into maps(map_name) values('Oregon');
insert into maps(map_name) values('UNKNOWN');

insert into match_types(type_name) values('scrim');
insert into match_types(type_name) values('qualifier');
insert into match_types(type_name) values('league');