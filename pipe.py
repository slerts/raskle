#!/usr/bin/python3
"""
pipe.py - pipes data from NHL stats api endpoints
author: Nick Seelert
email: nickseelert@gmail.com
"""

import json
from urllib.request import urlopen

baseURL = 'http://statsapi.web.nhl.com/api/v1'


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
    gets the team object for the id parameter from teams endpoint
    this endpoint includes teams that are no longer active
    if api still exists after expansion, this may break!
    :param team_id: team id number to grab from endpoint
    :return: json object from endpoint
    """
    url = baseURL + '/teams/' + str(team_id)
    return get_data(url)


def get_person(person_id):
    """
    gets the person object for the id parameter from the persons endpoint
    persons include players, coaches, and officials... maybe more but haven't
    investigated beyond these
    :param person_id: person if number to grab from endpoint
    :return: json object from endpoint
    """
    url = baseURL + '/people/' + str(person_id)
    return get_data(url)


def get_division(division_id):
    """
    gets the division object for the id parameter from the divisions endpoint
    includes historical divisions which are now inactive as well as world cup
    of hockey divisions which are also labelled inactive
    :param division_id: division id number to grab from endpoint
    :return: json object from endpoint
    """
    url = baseURL + '/divisions/' + str(division_id)
    return get_data(url)


def get_conference(conference_id):
    """
    gets the conference object for the id parameter from the conferences endpoint
    includes historical divisions which are now inactive as well as world cup
    of hockey convferences which are also labelled inactive
    :param conference_id: division id number to grab from endpoint
    :return: json object from endpoint
    """
    url = baseURL + '/conferences/' + str(conference_id)
    return get_data(url)


def get_franchise(franchise_id):
    """
    gets the franchise object for the id parameter from the franchises endpoint
    includes defunct franchises as well as a placeholder for Las Vegas expansion
    team planned for 2017 season
    :param franchise_id: division id number to grab from endpoint
    :return: json object from endpoint
    """
    url = baseURL + '/franchises/' + str(franchise_id)
    return get_data(url)


def get_game(game_id):
    """
    gets the game object for the id parameter from the live game feed endpoint
    :param game_id: game id number to grab from endpoint
    :return: json object from endpoint
    """
    url = baseURL + '/game/' + str(game_id) + '/feed/live'
    return get_data(url)