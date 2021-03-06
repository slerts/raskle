#!/usr/bin/python3
"""
store_data.py - adds data to mongoDB

author: Nick Seelert <nickseelert@gmail.com>
"""

# import datetime
from cache import mongo_connect as mc
from cache import pipe


games_coll = mc.db.games
update_coll = mc.db.update
# roster_coll = mc.db.rosters
# pstats_coll = mc.db.player_stats
# tstats_coll = mc.db.team_stats


def add_game(game_id):
    """
    add json object returned from pipe for requested game id

    :param game_id: id for game requested
    :return: inserted object id
    """
    game = pipe.get_game(game_id)
    return games_coll.insert_one(game).inserted_id


# def add_roster(team_abbr):
#     """
#     add json object returned from pipe for requested roster id
#
#     :param team_abbr: team abbreviation for roster requested
#     :return: inserted object id
#     """
#     roster = pipe.get_roster(team_abbr)
#     return roster_coll.insert_one(roster).inserted_id
#
#
# def add_player_stats(team_abbr, years, season_id):
#     """
#     add json object returned from pipe for requested team and the specified
#     season years and id
#
#     :param team_abbr: team abbreviation
#     :param season_id: dictates regular season (2) or playoffs (3)
#     :param years: start _S_ and end years _E_ for season requested (SSSSEEEE)
#     :return: inserted object id
#     """
#     pstats = pipe.get_playerstats_by_team(team_abbr, years, season_id)
#     pstats['team'] = team_abbr
#     return pstats_coll.insert_one(pstats).inserted_id
#
#
# def add_team_stats():
#     """
#     adds json object returned from pipe for all teams stats
#
#     :return: inserted object id
#     """
#     tstats = pipe.get_team_stats()
#     tstats['timestamp'] = datetime.datetime.utcnow()
#     return tstats_coll.insert_one(tstats).inserted_id
