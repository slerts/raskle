#!/usr/bin/python3
"""
update_db.py - initializes the db

all that is needed at this point is game data
other functions that are commented out are included if data is required in the future

author: Nick Seelert <nickseelert@gmail.com>
"""

import datetime

from cache import store_data, pipe

with open('gameday.txt') as a_file:
    gameday_array = a_file.read().split("-")

gameday = datetime.date(gameday_array[0], gameday_array[1], gameday_array[2])
today = datetime.date.today()

# team_list = ['BOS', 'BUF', 'DET', 'FLA', 'MTL', 'OTT', 'TBL', 'TOR',
#             'CAR', 'CBJ', 'NJD', 'NYI', 'NYR', 'PHI', 'PIT', 'WSH',
#             'CHI', 'COL', 'DAL', 'MIN', 'NSH', 'STL', 'WPG',
#             'ANA', 'ARI', 'CGY', 'EDM', 'LAK', 'SJS', 'VAN']


#def init_tstats():
#    """
#    initiates team stats collection
#    :return: NONE
#    """
#    tstats_id = store_data.add_team_stats()
#    print('\tStored object: ' + tstats_id.__str__())



#def init_rosters_stats():
#    """
#    initiates the rosters and player stats collections
#    assumes regular season (2) and current season (20162017)
#    :return: NONE
#    """
#    for team in team_list:
#        roster_id = store_data.add_roster(team)
#        pstats_id = store_data.add_player_stats(team, 20162017, 2)
#        print('\tStored roster object: ' + roster_id.__str__())
#        print('\tStored player stats object: ' + pstats_id.__str__())


def update_games():
    """
    updates the games collection to include new games
    :return: None
    """
    gameday = today
    while gameday < today:
        print('\tAdding Games for ' + gameday.__str__())
        games = pipe.get_game_ids(gameday.__str__()).get('games')

        for game in games:
            gameobj_id = store_data.add_game(game.get('id'))
            print('\t\tStored game object: ' + gameobj_id.__str__())

        next_date = games.get('nextDate').split("/")
        gameday = datetime.date(next_date[2], next_date[0], next_date[1])

    with open('next_update.txt') as a_file:
        a_file.write(gameday.__str__())


if __name__ == "__main__":
    #print('Initializing Team Stats Collection...')
    #init_tstats()

    #print('Initializing Rosters and Player Stats Collections...')
    #init_rosters_stats()

    print('Initializing Game Stats Collection...')
    update_games()