#!/usr/bin/python3

import MySQLdb

# database credentials
dbname = 'nhl_stats'
dbuser = 'mysql'
dbpwd = None
dbhost = 'localhost'

db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpwd, db=dbname)

# connect to db and create cursor c
def get_cursor():
    return db.cursor()

def close():
    db.close()