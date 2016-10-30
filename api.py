#!/usr/bin/python3
"""
api.py - RESTful api to serve data from and write json documents to mongoDB
author: Nick Seelert
email: nickseelert@gmail.com
"""

import pipe

def store_object(data, collection):
    """
    takes a json data object and the collection to store it in
    :param data: json data file returned by pipe
    :param collection: the mongodb collection where data should be stored
    :return:
    """
    pass