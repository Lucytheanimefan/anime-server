from pymongo import MongoClient

from os import environ

import secrets

def get_db():
    client = MongoClient(environ.get('MONGODB_URI'))
    db = client[environ.get('CLIENT_MONGODB')]

    return db