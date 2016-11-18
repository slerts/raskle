#!/usr/bin/python3

import MySQLdb


# database credentials
dbname = 'nhl_stats'
dbuser = 'mysql'
dbpwd = None
dbhost = 'localhost'

# connect to db and create cursor c
db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpwd, db=dbname)
c = db.cursor()

# create tables
c.execute("""CREATE TABLE positions (
    position_code VARCHAR(3),
    name VARCHAR(16),
    type VARCHAR(16),
    abbreviation VARCHAR(3),
    PRIMARY KEY(position_code))""")

c.execute("""CREATE TABLE people (
    pid INT,
    first_name VARCHAR(32),
    last_name VARCHAR(64),
    jersey_number INT,
    birthday DATE,
    height VARCHAR(8),
    weight INT,
    shoots_catches CHAR(1),
    position_code VARCHAR(3),
    PRIMARY KEY (player_id),
    FOREIGN KEY (position_code) REFERENCES positions(position_code))""")

c.execute("""CREATE TABLE conferences (
    conference_id INT,
    name VARCHAR(64),
    abbreviation CHAR(30),
    PRIMARY KEY (conference_id)""")

c.execute("""CREATE TABLE divisions (
    division_id INT,
    name VARCHAR(64),
    abbreviation CHAR(30),
    conference_id INT,
    PRIMARY KEY(division_id),
    FOREIGN KEY (conference_id) REFERENCES conferences(conference_id))""")

c.execute("""CREATE TABLE teams (
    team_id INT,
    full_name VARCHAR(64),
    abbreviation CHAR(3),
    team_name VARCHAR(32),
    division_id INT,
    conference_id INT,
    PRIMARY KEY (team_id),
    FOREIGN KEY (division_id) REFERENCES divisions(division_id),
    FOREIGN KEY (conference_id) REFERENCES conferences(conference_id))""")

c.execute("""CREATE TABLE games (
    game_id INT NOT NULL,
    start_date_time DATETIME,
    end_date_time DATETIME,
    home_team_id INT,
    away_team_id INT,
    arena VARCHAR(128),
    has_shootout BOOLEAN,
    first_star_pid INT,
    second_star_pid INT,
    third_star_pid INT,
    PRIMARY KEY (game_id),
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (first_star_pid) REFERENCES people(pid),
    FOREIGN KEY (second_star_pid) REFERENCES people(pid),
    FOREIGN KEY (third_star_pid) REFERENCES people(pid)""")

c.execute("""CREATE TABLE pp_stats (
    game_id INT,
    home_pp_pct REAL,
    home_pp_goals INT,
    home_pp_opp INT,
    away_pp_pct REAL,
    away_pp_goals INT,
    away_pp_opp INT,
    PRIMARY KEY (game_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id))""")

c.execute("""CREATE TABLE rosters (
    game_id INT,
    player_id INT,
    team_id INT,
    scratched VARCHAR(10),
    PRIMARY KEY (game_id, player_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id)
    FOREIGN KEY (player_id) REFERENCES people(pid),
    FOREIGN KEY (team_id) REFERENCES teams(team_id))""")

c.execute("""CREATE TABLE time_on_ice (
    game_id INT,
    player_id INT,
    toi TIME,
    even_toi TIME,
    sh_toi TIME,
    PRIMARY KEY (game_id, player_id),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (player_id) REFERENCES people(pid))""")

c.execute("""CREATE TABLE plays (
    game_id INT,
    date_time DATETIME,
    event_idx INT,
    team_id INT,
    period INT,
    period_time TIME,
    x_coord REAL,
    y_coord REAL,
    home_score INT,
    away_score INT,
    PRIMARY KEY (game_id, event_idx),
    FOREIGN KEY (game_id) REFERENCES games(game_id))""")

c.execute("""CREATE TABLE shots (
    game_id INT,
    event_idx INT,
    shooter_pid INT,
    goalie_pid INT,
    shot_type VARCHAR(64),
    PRIMARY KEY(game_id, event_idx),
    FOREIGN KEY (game_id, event_idx) REFERENCES plays(game_id, event_idx),
    FOREIGN KEY (shooter_pid) REFERENCES people(pid),
    FOREIGN KEY (goalie_pid) REFERENCES people(pid))""")

c.execute("""CREATE TABLE missed_shots (
    game_id INT,
    event_idx INT,
    shooter_pid INT,
    PRIMARY KEY(game_id, event_idx),
    FOREIGN KEY (game_id, event_idx) REFERENCES plays(game_id, event_idx),
    FOREIGN KEY (shooter_pid) REFERENCES people(pid))""")

c.execute("""CREATE TABLE blocked_shots (
    game_id INT,
    event_idx INT,
    shooter_pid INT,
    blocker_pid INT,
    PRIMARY KEY(game_id, event_idx),
    FOREIGN KEY (game_id, event_idx) REFERENCES plays(game_id, event_idx),
    FOREIGN KEY (shooter_pid) REFERENCES people(pid),
    FOREIGN KEY (blocker_pid) REFERENCES people(pid))""")

c.execute("""CREATE TABLE goals (
    game_id INT,
    event_idx INT,
    shooter_pid INT,
    assist_1_pid INT,
    assist_2_pid INT,
    goalie_pid INT,
    shot_type VARCHAR(64),
    empty_net BOOLEAN,
    game_winner BOOLEAN,
    PRIMARY KEY(game_id, event_idx),
    FOREIGN KEY (game_id, event_idx) REFERENCES plays(game_id, event_idx),
    FOREIGN KEY (shooter_pid) REFERENCES people(pid),
    FOREIGN KEY (assist_1_pid) REFERENCES people(pid),
    FOREIGN KEY (assist_2_pid) REFERENCES people(pid),
    FOREIGN KEY (goalie_pid) REFERENCES people(pid))""")

c.execute("""CREATE TABLE penalties (
    game_id INT,
    event_idx INT,
    penalty_on_pid INT,
    drawn_by_pid INT,
    penalty_minutes INT,
    penalty_severity VARCHAR(16),
    penalty_type VARCHAR(32),
    PRIMARY KEY(game_id, event_idx),
    FOREIGN KEY (game_id, event_idx) REFERENCES plays(game_id, event_idx),
    FOREIGN KEY (penalty_on_pid) REFERENCES people(pid),
    FOREIGN KEY (drawn_by_pid) REFERENCES people(pid))""")

c.execute("""CREATE TABLE faceoffs (
    game_id INT,
    event_idx INT,
    winner_pid INT,
    loser_pid INT,
    PRIMARY KEY(game_id, event_idx),
    FOREIGN KEY (game_id, event_idx) REFERENCES plays(game_id, event_idx),
    FOREIGN KEY (winner_pid) REFERENCES people(pid),
    FOREIGN KEY (loser_pid) REFERENCES people(pid))""")

c.execute("""CREATE TABLE poss_changes (
    game_id INT,
    event_idx INT,
    player_id INT,
    change_type CHAR(8),
    PRIMARY KEY(game_id, event_idx),
    FOREIGN KEY (game_id, event_idx) REFERENCES plays(game_id, event_idx),
    FOREIGN KEY (player_pid) REFERENCES people(pid))""")

c.execute("""CREATE TABLE hits (
    game_id INT,
    event_idx INT,
    hitter_pid INT,
    hittee_pid INT,
    PRIMARY KEY(game_id, event_idx),
    FOREIGN KEY (game_id, event_idx) REFERENCES plays(game_id, event_idx),
    FOREIGN KEY (hitter_pid) REFERENCES people(pid),
    FOREIGN KEY (hittee_pid) REFERENCES people(pid))""")

c.execute("""CREATE TABLE stoppages (
    game_id INT,
    event_idx INT,
    description VARCHAR(200),
    PRIMARY KEY(game_id, event_idx),
    FOREIGN KEY (game_id, event_idx) REFERENCES plays(game_id, event_idx))""")


