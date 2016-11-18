#!/usr/bin/python3
"""
init_db.py - initializes the db to the current date when starting out

author: Nick Seelert <nickseelert@gmail.com>
"""

import datetime

import pipe
from mirror import store_data

season_start = datetime.date(2016, 10, 12)
today = datetime.date.today()
team_list = ['BOS', 'BUF', 'DET', 'FLA', 'MTL', 'OTT', 'TBL', 'TOR',
             'CAR', 'CBJ', 'NJD', 'NYI', 'NYR', 'PHI', 'PIT', 'WSH',
             'CHI', 'COL', 'DAL', 'MIN', 'NSH', 'STL', 'WPG',
             'ANA', 'ARI', 'CGY', 'EDM', 'LAK', 'SJS', 'VAN']


def init_tstats():
    """
    initiates team stats collection
    :return: NONE
    """
    tstats_id = store_data.add_team_stats()
    print('\tStored object: ' + tstats_id.__str__())



def init_rosters_stats():
    """
    initiates the rosters and player stats collections
    assumes regular season (2) and current season (20162017)
    :return: NONE
    """
    for team in team_list:
        roster_id = store_data.add_roster(team)
        pstats_id = store_data.add_player_stats(team, 20162017, 2)
        print('\tStored roster object: ' + roster_id.__str__())
        print('\tStored player stats object: ' + pstats_id.__str__())


def init_games():
    """
    initiates the games collection
    :return: NONE
    """
    gameday = season_start
    while gameday < today:
        print('\tAdding Games for ' + gameday.__str__())
        games = pipe.get_game_ids(gameday.__str__()).get('games')

        for game in games:
            gameobj_id = store_data.add_game(game.get('id'))
            print('\t\tStored game object: ' + gameobj_id.__str__())

        gameday += datetime.timedelta(days=1)

if __name__ == "__main__":
    print('Initializing Team Stats Collection...')
    init_tstats()

    print('Initializing Rosters and Player Stats Collections...')
    init_rosters_stats()

    print('Initializing Game Stats Collection...')
    init_games()