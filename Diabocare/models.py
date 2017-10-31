import os
from pymongo import MongoClient

from application import app

DATABASE_URI = 'mongodb://diabocare:swe123@ds159254.mlab.com:59254/diabocare'

DATABASE = MongoClient(DATABASE_URI)
db = DATABASE.get_default_database()




# app.config['MONGO_DBNAME'] = 'diabocare'  
# app.config['MONGO_URI'] = 'mongodb://diabocare:swe123@ds159254.mlab.com:59254/diabocare'

# db = PyMongo(app)

USERS_COLLECTION = db.users
READING_COLLECTION = db.readings
doctor_USERS_COLLECTION = db.doctorusers

