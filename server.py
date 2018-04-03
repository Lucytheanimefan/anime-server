from pymongo import MongoClient
#from config import *
#from boto.s3.connection import S3Connection

from os import environ


#s3 = S3Connection(os.environ['PROD_MONGODB'], os.environ['CLIENT_MONGODB'])

def get_db():
    client = MongoClient(environ.get('MONGODB_URI'))
    db = client[environ.get('CLIENT_MONGODB')]

    return db