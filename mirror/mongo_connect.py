#!/usr/bin/python3
"""
mongo_connect.py -- used to connect with local mongoDB

"""
from pymongo import MongoClient

db_name = 'raskle'

client = MongoClient('localhost', 27017)

# MongoDB creates db if it doesn't already exist
db = client.raskle

