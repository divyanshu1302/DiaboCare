import os
from pymongo import MongoClient

from application import app

DATABASE_URI = ''

DATABASE = MongoClient(DATABASE_URI)
db = DATABASE.get_default_database()

USERS_COLLECTION = db.users
READING_COLLECTION = db.readings
doctor_USERS_COLLECTION = db.doctorusers

