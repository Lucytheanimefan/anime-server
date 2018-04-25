from pymongo import MongoClient

from os import environ

import secrets

def get_db():
    client = MongoClient(environ.get('MONGODB_URI'))
    db = client[environ.get('CLIENT_MONGODB')]
    
    # client = MongoClient('mongodb://heroku_sjwpcpmp:bot3lu7crprs0qm1mhdsv40pv7@ds121091.mlab.com:21091/heroku_sjwpcpmp')
    # db = client['heroku_sjwpcpmp']

    return db