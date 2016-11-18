#!/usr/bin/python3
"""
save_game.py - extracts data of interest from game data

play by play events start from 2010

events of interest:
    even strength: shots, blocked shots, missed shots, goals, sv pct %
    other: pp %, pk %, shooting %

author: Nick Seelert <nickseelert@gmail.com>
"""

import pipe
import MySQLdb
from datetime import time, datetime, timedelta, tzinfo


# database credentials
dbname = 'nhl_stats'
dbuser = 'mysql'
dbpwd = None
dbhost = 'localhost'

# connect to db and create cursor c
db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpwd, db=dbname)
c = db.cursor()

def convert_time(time_string):
    """
    reformats the time_string to MySQL DATETIME format
    :param time_string: date and time string
    :return:
    """
    dt_array = time_string.split('T')
    return dt_array[0] + " " + dt_array[1][:-1]


def extract_events(game_id):
    """
    extracts required collections from the game object param and passes to proper function

    :param game_id: json game object
    :return:
    """
    game = pipe.get_game(game_id)
    gamedata = game.get('gameData')
    decisions = game.get('liveData').get('decisions')
    linescore = game.get('liveData').get('linescore')
    teams = game.get('liveData').get('boxscore').get('teams')
    play_by_play = game.get('liveData').get('plays').get('allPlays')

    store_gamedata(game_id, gamedata, decisions, linescore)
    store_ppstats(game_id, teams)
    store_rosters(game_id, teams)
    store_toi(game_id, teams)
    store_plays(game_id, play_by_play)


def store_gamedata(game_id, gamedata, decisions, linescore):
    start_date_time = convert_time(gamedata.get('gameData').get('datetime').get('dateTime'))
    end_date_time = convert_time(gamedata.get('gameData').get('datetime').get('endDateTime'))
    home_team_id = gamedata.get('gameData').get('teams').get('home').get('id')
    away_team_id = gamedata.get('gameData').get('teams').get('away').get('id')
    arena = gamedata.get('gameData').get('venue').get('name')
    has_shootout = linescore.get('hasShootout')
    first_star_pid = decisions.get('firstStar').get('id')
    second_star_pid = decisions.get('secondStar').get('id')
    third_star_pid = decisions.get('thirdStar').get('id')
    c.execute(
        """INSERT INTO games (game_id, start_date_time, end_date_time, home_team_id, away_team_id, arena,
        has_shootout, first_star_pid, second_star_pid, third_star_pid)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (game_id, start_date_time, end_date_time, home_team_id, away_team_id, arena,
         has_shootout, first_star_pid, second_star_pid, third_star_pid))


def store_ppstats(game_id, teams):
    home_pp_pct = teams.get('home').get('teamStats').get('teamSkaterStats').get('powerPlayPercentage')
    home_pp_goals = teams.get('home').get('teamStats').get('teamSkaterStats').get('powerPlayGoals')
    home_pp_opp = teams.get('home').get('teamStats').get('teamSkaterStats').get('powerPlayOpportunities')
    away_pp_pct = teams.get('away').get('teamStats').get('teamSkaterStats').get('powerPlayPercentage')
    away_pp_goals = teams.get('away').get('teamStats').get('teamSkaterStats').get('powerPlayGoals')
    away_pp_opp = teams.get('away').get('teamStats').get('teamSkaterStats').get('powerPlayOpportunities')
    c.execute(
        """INSERT INTO pp_stats (game_id, home_pp_pct, home_pp_goals, home_pp_opp, away_pp_pct, away_pp_goals, away_pp_opp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (game_id, home_pp_pct, home_pp_goals, home_pp_opp, away_pp_pct, away_pp_goals, away_pp_opp))


def store_rosters(game_id, teams):

    def store_player(player_id, team_id, scratched):
        c.execute(
            """INSERT INTO rosters (game_id, player_id, team_id, scratched)
            VALUES (%s, %s, %s, %s)""", (game_id, player_id, team_id, scratched))

    for team in teams:
        team_id = team.get('team').get('id')
        players = team.get('skaters') + team.get('goalies')
        scratches = team.get('scratches')
        scratch = False

        for player_id in players:
            if player_id in scratches:
                scratch = True

            store_player(player_id, team_id, scratch)


def store_toi(game_id, teams):

    def store_player(player):
        player_id = player.get('person').get('id')
        toi = "00:" + player.get('stats').get('skaterStats').get('timeOnIce')
        even_toi = "00:" + player.get('stats').get('skaterStats').get('evenTimeOnIce')
        pp_toi = "00:" + player.get('stats').get('skaterStats').get('powerPlayTimeOnIce')
        sh_toi = "00:" + player.get('stats').get('skaterStats').get('shortHandedTimeOnIce')
        c.execute(
            """INSERT INTO time_on_ice (game_id, player_id, toi, even_toi, pp_toi, sh_toi)
            VALUES (%s, %s, %s, %s, %s, %s)""", (game_id, player_id, toi, even_toi, pp_toi, sh_toi))

    home_team = teams.get('home').get('players')
    away_team = teams.get('away').get('players')

    for player in home_team:
        store_player(player)

    for player in away_team:
        store_player(player)


def store_plays(game_id, pbp):
    """
    saves each play from json object to proper table in SQL db

        :param pbp: play by play collection passed from extract_events()
        :return:
    """

    for play in pbp:
        play_type = play.get('result').get('eventTypeID')
        date_time = convert_time(play.get('about').get('dateTime'))
        event_idx  = play.get('about').get('eventIdx')
        team_id = play.get('team').get('id')
        period = play.get('about').get('period')
        period_time = "00:" + play.get('about').get('periodTime')
        x_coord = play.get('coordinates').get('x')
        y_coord = play.get('coordinates').get('y')
        home_score = play.get('about').get('goals').get('home')
        away_score = play.get('about').get('goals').get('away')

        c.execute("""INSERT INTO shots (game_id, date_time, event_idx, team_id, period, period_time,
        x_coord, y_coord, home_score, away_score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (game_id, date_time, event_idx, period, period_time, x_coord, y_coord, home_score, away_score, team_id))

        # record the play to the appropriate table
        if play_type == 'SHOT':

            for player in play.get('players'):
                if player.get('playerType') == 'Shooter':
                    shooter_pid = player.get('player').get('id')
                else:
                    goalie_pid = player.get('player').get('id')

            shot_type = play.get('result').get('secondaryType')

            c.execute("""INSERT INTO shots (game_id, event_idx, shooter_pid, goalie_pid, shot_type)
            VALUES (%s, %s, %s, %s, %s)""", (game_id, event_idx, shooter_pid, goalie_pid, shot_type))

        elif play_type == 'MISSED_SHOT':
            shooter_player_pid = player.get('player').get('id')

            c.execute("""INSERT INTO missed_shots (game_id, event_idx, shooter_player_pid)
            VALUES (%s, %s, %s)""", (game_id, event_idx, shooter_player_pid))

        elif play_type == 'BLOCKED_SHOT':
            for player in play.get('players'):
                if player.get('playerType') == 'Shooter':
                    shooter_player_pid = player.get('player').get('id')
                else:
                    blocker_player_pid = player.get('player').get('id')

            c.execute("""INSERT INTO blocked_shots (game_id, event_idx, shooter_player_pid, blocker_player_pid)
            VALUES (%s, %s, %s, %s)""", (game_id, event_idx, shooter_player_pid, blocker_player_pid))

        elif play_type == 'GOAL':
            shot_type = play.get('result').get('secondaryType')
            empty_net = play.get('result').get('isEmptyNet')
            game_winner = play.get('result').get('isGameWinningGoal')

            for player in play.get('players'):
                # scorer is the only player guaranteed to be included
                assist_pid1 = None
                assist_pid2 = None
                goalie_pid = None

                if player.get('playerType') == "Scorer":
                    scorer_pid = player.get('player').get('id')
                elif player.get('playerType') == "Assist":
                    if assist_pid1 is None:
                        assist_pid1 = player.get('player').get('id')
                    else:
                        assist_pid2 = player.get('player').get('id')
                elif player.get('playerType') == "Goalie":
                    goalie_pid = player.get('player').get('id')

                c.execute("""INSERT INTO goals (game_id, event_idx, scorer_pid, assist_pid1, assist_pid2, goalie_pid,
                shot_type, empty_net, game_winner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (game_id, event_idx, scorer_pid, assist_pid1, assist_pid2, goalie_pid, shot_type, empty_net,
                 game_winner))

        elif play_type == 'PENALTY':
            for player in play.get('players'):
                if player.get('playerType') == 'PenaltyOn':
                    penalty_on_pid = player.get('player').get('id')
                else:
                    drawn_by_pid = player.get('player').get('id')

            penalty_type = play.get('result').get('secondaryType')
            penalty_minutes = play.get('result').get('penaltyMinutes')
            penalty_severity = play.get('result').get('penaltySeverity')

            c.execute("""INSERT INTO penalties (game_id, event_idx, penalty_on_pid, drawn_by_pid, penalty_type,
            penalty_minutes, penalty_severity) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (game_id, event_idx, penalty_on_pid, drawn_by_pid, penalty_type, penalty_minutes, penalty_severity))

        elif play_type == 'FACEOFF':
            for player in play.get('players'):
                if player.get('playerType') == 'Winner':
                    winner_pid = player.get('player').get('id')
                else:
                    loser_pid = player.get('player').get('id')

            c.execute("""INSERT INTO faceoff (game_id, event_idx, winner_pid, loser_pid) VALUES (%s, %s, %s, %s)""",
            (game_id, event_idx, winner_pid, loser_pid))

        elif play_type == 'GIVEAWAY' or play_type == 'TAKEAWAY':
            player_id = play.get('players')[0].get('player').get('id')

            if play.get('result').get('event') == 'Takeaway':
                change_type = 'Takeaway'
            else:
                change_type = 'Giveaway'

            c.execute("""INSERT INTO poss_changes (game_id, event_idx, player_id, change_type)
            VALUES (%s, %s, %s, %s)""", (game_id, event_idx, player_id, change_type))

        elif play_type == 'HIT':
            for player in play.get('players'):
                if player.get('playerType') == 'Hitter':
                    hitter_pid = player.get('player').get('id')
                else:
                    hittee_pid = player.get('player').get('id')

            c.execute("""INSERT INTO faceoff (game_id, event_idx, hitter_pid, loser_pid)
            VALUES (%s, %s, %s, %s)""", (game_id, event_idx, hitter_pid, hittee_pid))

        elif play_type == 'STOP':
            description = play.get('result').get('description')

            c.execute("""INSERT INTO faceoff (game_id, event_idx, description)
            VALUES (%s, %s, %s)""", (game_id, event_idx, description))
