CREATE TABLE players (
    player_id serial PRIMARY KEY,
    player_name VARCHAR(20) NOT NULL
);

CREATE TABLE team_names (
    team_id serial PRIMARY KEY,
    team_name VARCHAR(50)
);

CREATE TABLE teams (
    team_id serial,
    player_id integer,
    name_id integer REFERENCES team_names(team_id),
    PRIMARY KEY(team_id, player_id),
    CONSTRAINT plaryer_exists FOREIGN KEY(player_id) REFERENCES players(player_id)
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
    team_id integer,
    map_id integer,
    match_type_id integer,
    rounds_won integer,
    rounds_lost integer,
    score_at_half integer,
    attacker_start boolean,
    CONSTRAINT matches_map_exists FOREIGN KEY(map_id) REFERENCES maps(map_id),
    CONSTRAINT matches_match_type_exists FOREIGN KEY(match_type_id) REFERENCES match_types(type_id),
    CONSTRAINT analyst_identifier_is_unique UNIQUE(analyst_identifier)
);

CREATE TABLE stats (
    stat_id serial PRIMARY KEY,
    player_id integer,
    match_id integer,
    map_id integer,
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
insert into maps(map_name) values('Kafe Dostoyevsky');
insert into maps(map_name) values('Chalet');
insert into maps(map_name) values('Oregon');
insert into maps(map_name) values('UNKNOWN');

insert into match_types(type_name) values('scrim');
insert into match_types(type_name) values('qualifier');
insert into match_types(type_name) values('league');