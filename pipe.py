#!/usr/bin/python3
"""
pipe.py - pipes data from NHL stats api endpoints
author: Nick Seelert
email: nickseelert@gmail.com
"""

import json
import xml.etree.ElementTree as ET
from urllib.request import urlopen


base_url = {'statsapi': 'http://statsapi.web.nhl.com/api/v1',
           'nhlwc': 'http://nhlwc.cdnak.neulion.com/fs1/nhl/league',
           'gameday': 'http://live.nhle.com/GameData/GCScoreboard'}


### NHL STATS API ENDPOINTS ###
# each team is assigned a team id number by NHL.com
# I don't know if there is a pattern for assignment

def get_data(url):
    """
    get_data grabs the json data from the desired endpoint

    :param url: full url for endpoint
    :return: returns the json object
    """
    resp = urlopen(url).read()
    return json.loads(resp.decode('utf-8'))


def get_team(team_id):
    """
    gets the basic team data for the id parameter from teams endpoint
    this endpoint includes teams that are no longer active
    if api still exists after expansion, this may break!

    :param team_id: team id number to grab from endpoint
    :return: json object from endpoint
    """
    url = base_url['statsapi'] + '/teams/' + str(team_id)
    return get_data(url)


def get_person(person_id):
    """
    gets the person object for the id parameter from the persons endpoint
    persons include players, coaches, and officials... maybe more but haven't
    investigated beyond these

    :param person_id: person if number to grab from endpoint
    :return: json object from endpoint
    """
    url = base_url['statsapi'] + '/people/' + str(person_id)
    return get_data(url)


def get_division(division_id):
    """
    gets the division object for the id parameter from the divisions endpoint
    includes historical divisions which are now inactive as well as world cup
    of hockey divisions which are also labelled inactive

    :param division_id: division id number to grab from endpoint
    :return: json object from endpoint
    """
    url = base_url['statsapi'] + '/divisions/' + str(division_id)
    return get_data(url)


def get_conference(conference_id):
    """
    gets the conference object for the id parameter from the conferences endpoint
    includes historical divisions which are now inactive as well as world cup
    of hockey conferences which are also labelled inactive

    :param conference_id: division id number to grab from endpoint
    :return: json object from endpoint
    """
    url = base_url['statsapi'] + '/conferences/' + str(conference_id)
    return get_data(url)


def get_franchise(franchise_id):
    """
    gets the franchise object for the id parameter from the franchises endpoint
    includes defunct franchises as well as a placeholder for Las Vegas expansion
    team planned for 2017 season

    :param franchise_id: division id number to grab from endpoint
    :return: json object from endpoint
    """
    url = base_url['statsapi'] + '/franchises/' + str(franchise_id)
    return get_data(url)


def get_game(game_id):
    """
    gets the game object for the id parameter from the live game feed endpoint

    :param game_id: game id number to grab from endpoint
    :return: json object from endpoint
    """
    url = base_url['statsapi'] + '/game/' + str(game_id) + '/feed/live'
    return get_data(url)


### NHLWC CDN ENDPOINTS ###
# Uses team abbreviation rather than team id# (ex. ANA)

def get_roster(team_abbr):
    """
    gets the team roster for the given team abbreviation

    :param team_abbr: team abbreviation
    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/teamroster/' + str(team_abbr) + '/iphone/clubroster.json'
    return get_data(url)


def get_sched(team_abbr, year, month):
    """
    gets the team schedule for the given team abbreviation

    :param team_abbr: team abbreviation
    :param year: year (YYYY) for schedule requested
    :param month: month (MM) for schedule requested
    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/clubschedule/' + str(team_abbr) + '/' + str(year) + '/' + str(month) \
          + '/iphone/clubschedule.json'
    return get_data(url)


def get_playerstats_by_team(team_abbr, years, season_id):
    """
    gets player stats for an entire team for the given team abbreviation

    :param team_abbr: team abbreviation
    :param season_id: dictates regular season (2) or playoffs (3)
    :param years: start _S_ and end years _E_ for season requested (SSSSEEEE)
    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/playerstatsline/' + str(years) + '/' + str(season_id) + '/' + str(team_abbr) \
          + '/iphone/playerstatsline.json'
    return get_data(url)


def get_ll_pts():
    """
    gets league leaders in points

    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/leagueleaders/iphone/points/leagueleaders.json'
    return get_data(url)


def get_ll_goals():
    """
    gets league leaders in goals

    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/leagueleaders/iphone/goals/leagueleaders.json'
    return get_data(url)


def get_ll_assists():
    """
    gets league leaders in assists

    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/leagueleaders/iphone/assists/leagueleaders.json'
    return get_data(url)


def get_ll_plusminus():
    """
    gets league leaders in plus/minus

    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/leagueleaders/iphone/plusminus/leagueleaders.json'
    return get_data(url)


def get_ll_wins():
    """
    gets league leaders in wins (goalies)

    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/leagueleaders/iphone/wins/leagueleaders.json'
    return get_data(url)


def get_ll_gaa():
    """
    gets league leaders in goals against average (goalies)

    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/leagueleaders/iphone/gaa/leagueleaders.json'
    return get_data(url)

def get_ll_sv_pct():
    """
    gets league leaders in save percentage (goalies)

    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/leagueleaders/iphone/savepercentage/leagueleaders.json'
    return get_data(url)


def get_ll_so():
    """
    gets league leaders in shutouts (goalies)

    :return: json object from endpoint
    """
    url = base_url['nhlwc'] + '/leagueleaders/iphone/shutouts/leagueleaders.json'
    return get_data(url)


### NHL Live endpoint ###
# used to get game ids for each day
# DOESN'T WORK: END POINT DOESN'T SERVE PROPER JSON OBJECT

def get_game_ids(day):
    """
    gets all game ids for a specific day
    can't use general get_data(url) function because endpoint doesn't return a valid json object
    need to slice out part of string before returning

    :param day: gameday requested (YYYY-MM-DD)
    :return: json object from endpoint
    """
    url = base_url['gameday'] + '/' + str(day) + '.jsonp'
    resp = urlopen(url).read()
    return json.loads(resp[15:-2].decode('utf-8'))

### MISC One off Endpoints ###
# these endpoints are one offs and don't require a baseURL

def get_team_stats():
    """
    gets the current standings
    endpoint serves XML format not JSON, need to convert to json before passing back

    :return: converted json object from xml object endpoint
    """
    url = 'http://app.cgy.nhl.yinzcam.com/V2/Stats/Standings'
    resp = urlopen(url).read()
    root = ET.fromstring(resp)

    # convert XML to json before passing back to api
    confs = {}
    for conf in root.findall("Conference"):
        divs = {}

        for div in conf.findall("StatsSection"):
            teams = []

            for squad in div.findall("Standing"):
                stats1 = squad.find("StatsGroup[@Order='1']")
                stats2 = squad.find("StatsGroup[@Order='2']")
                teams.append({
                    "id": squad.get("Id"),
                    "team": squad.get("Team"),
                    "abbr": squad.get("TriCode"),
                    "leagueRank": squad.get("LeagueRank"),
                    "conferenceRank": squad.get("ConfRank"),
                    "divisionRank": squad.get("DivRank"),
                    "gamesPlayed": stats1.get("Stat0"),
                    "wins": stats1.get("Stat1"),
                    "losses": stats1.get("Stat2"),
                    "overtimeLosses": stats1.get("Stat3"),
                    "points": stats1.get("Stat4"),
                    "goalsFor": stats2.get("Stat0"),
                    "goalsAgainst": stats2.get("Stat1"),
                    "lastTen": stats2.get("Stat2"),
                    "streak": stats2.get("Stat3")
                })

            divs[div.attrib.get('Heading')] = teams

        confs[conf.attrib.get('Name')] = {'division': divs}

    return {'conferences': confs}
