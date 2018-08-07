from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from Diabocare import views 
