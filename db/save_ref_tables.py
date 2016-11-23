#!/usr/bin/python3
"""
save_ref_tables.py - saves data for reference tables

positions, people, teams, divisions, conferences

author: Nick Seelert <nickseelert@gmail.com>
"""

from db import sql_connect as db
from db import parser

sql = db.get_cursor()


def store_positions(positions):
    for p in positions:
        position_code = p.get('position_code')
        name = p.get('name')
        pos_type = p.get('pos_type')
        abbreviation = p.get('abbreviation')
        sql.execute(
            """INSERT INTO positions (position_code, name, pos_type, abbreviation)
            VALUES (%s, %s, %s, %s)""", (position_code, name, pos_type, abbreviation))


def store_player(pid):
    player = parser.get_person(pid)
    details = player.get('people')[0]
    first_name = details.get('firstName')
    last_name = details.get('lastName')
    jersey_number = details.get('primaryNumber')
    birthday = details.get('birthDate')
    height = details.get('height')
    weight = details.get('weight')
    shoots_catches = details.get('shootsCatches')
    position_code = player.get('people')[1].get('code')

    sql.execute(
        """INSERT INTO people (pid, first_name, last_name, jersey_number, birthday, height, weight,
        shoots_catches, position_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (pid, first_name, last_name, jersey_number, birthday, height, weight, shoots_catches, position_code))


def store_conference(conference_id):
    conference = parser.get_conference(conference_id).get('conferences')[0]
    name = conference.get('name')
    abbreviation = conference.get('abbreviation')

    sql.execute(
        """INSERT INTO conferences (conference_id, name, abbreviation) VALUES (%s, %s, %s)""",
        (conference_id, name, abbreviation))


def store_division(division_id):
    division = parser.get_division(division_id).get('divisions')[0]
    name = division.get('name')
    abbreviation = division.get('abbreviation')
    conference_id = division.get('conference').get('id')

    sql.execute(
        """INSERT INTO divisions (division_id, name, abbreviation, conference_id) VALUES (%s, %s, %s, %s)""",
        (division_id, name, abbreviation, conference_id))


def store_team(team_id):
    team = parser.get_team(team_id).get('teams')
    location = team.get('locationName')
    abbreviation = team.get('abbreviation')
    team_name = team.get('Bruins')
    division_id = team.get('division').get('id')
    conference_id = team.get('conference').get('id')

    sql.execute(
        """INSERT INTO teams (team_id, location, abbreviation, team_name, division_id, conference_id)
        VALUES (%s, %s, %s, %s, %s, %s)""", (team_id, location, abbreviation, team_name, division_id, conference_id))
