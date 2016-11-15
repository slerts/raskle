#!/usr/bin/python3
"""
munger.py - extracts data of interest from game data

play by play events start from 2010

events of interest:
    even strength: shots, blocked shots, missed shots, goals, sv pct %
    other: pp %, pk %, shooting %

author: Nick Seelert <nickseelert@gmail.com>
"""

import pipe
from datetime import time, timedelta


def extract_events(game_id):
    """
    extracts required collectioned from the game object param and passes to proper function

    :param game_id: json game object
    :return:
    """
    gamedata = pipe.get_game(game_id)
    teamdata = gamedata.get('liveData').get('boxscore').get('teams')
    play_by_play = gamedata.get('liveData').get('plays').get('allPlays')
    boxscore_data(teamdata)
    even_strength_events(play_by_play)

def boxscore_data(tdata):
    pass

def even_strength_events(pbp):
    """
    extracts the corsi events from the game object that is passed to the function

        :param pbp: play by play collection passed from extract_events()
        :return:
    """
    # tracks if game is currently even strength
    even_strength = True
    # end time for most recently penalty taken (team does not matter)
    penalty_end = time(0, 0, 0)
    # goal differential -- + values home team leads, - values away team
    goal_diff = 0

    for play in pbp:
        period = play.get('about').get('period')
        period_time_split = play.get('about').get('periodTime').split(':')
        period_time = time(0, period_time_split[0], period_time_split[1])
        play_type = play.get('result').get('eventTypeID')
        goal_diff = play.get('goals').get('home') - play.get('goals').get('away')

        # check if most recent penalty has expired and
        if even_strength == False and period_time > penalty_end:
            even_strength = True

        if even_strength and ((period < 3 and abs(goal_diff) < 2) or (period == 3 and abs(goal_diff) == 0)):

            if play_type == 'SHOT':
                # gameId, eventIdx, period, periodTime, team_id, team_tricode, coordinates, even_strength, shooter, goalie, type of shot
                pass
            elif play_type == 'MISSED_SHOT':
                # gameId, eventIdx, period, periodTime, team_id, team_tricode, coordinates, even_strength, shooter
                pass
            elif play_type == 'BLOCKED_SHOT':
                # gameId, eventIdx, period, periodTime, team_id, team_tricode, coordinates, even_strength,  shooter, blocker,
                pass
            elif play_type == 'GOAL' and play.get('result').get('isEmptyNet') != True:
                # gameId, eventIdx, period, periodTime, team_id, team_tricode coordinates, scorer, assist, assist, type of shot,
                pass
            elif play_type == 'PENALTY' and play.get('result').get('secondaryType') != ('Fighting' or 'Game Misconduct'):
                even_strength = False
                pim = play.get('result').get('penaltyMinutes')
                penalty_end = period_time + timedelta(minutes = pim)