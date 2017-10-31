from werkzeug.security import check_password_hash, generate_password_hash
from Diabocare.models import READING_COLLECTION
from flask_login import UserMixin

class Reading(UserMixin):

    def __init__(self, username, reading_date, value, mood,db=False):
        self.username = username
        self.reading_date = reading_date
        self.value = value
        self.mood = mood

        if db:
            READING_COLLECTION.insert_one({
                'postedBy': self.username, 'reading_date': self.reading_date,
                'value': self.value, 'mood': self.mood
                })

