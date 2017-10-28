from Diabocare.application import app, lm
import pymongo
import json
from flask import request, redirect, render_template, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from Diabocare.models import USERS_COLLECTION  

from Diabocare.user import User
from Diabocare.reading import Reading

from Diabocare.forms import LoginForm, SignUpForm  #, QuestionForm, AnswerForm
from bson.objectid import ObjectId


@app.route('/')
@app.route('/home/', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        a =  'You are logged in as ' + session['username']
        return render_template('index.html',a = a,current_user=current_user)
    return render_template('home.html',current_user=current_user, form = LoginForm())

'''@app.route('/profile/', methods=['GET'])
@login_required
def profile():
    user = USERS_COLLECTION.find_one({'_id': current_user.get_id()})
    ques, ans = [], []
    for q_obj in user['quesPosted']:
        q = QuestionMethods(q_obj)
        ques.append(q.getQuestion())
    return redirect(url_for('home'))
    #return render_template('profile.html', title='HoverSpace | Profile', user=user)'''

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = USERS_COLLECTION.find_one({ "_id": form.username.data })
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            session['username'] = form.username.data
            login_user(user_obj, remember=True)
            flash("Logged in successfully!", category='success')
            return redirect(url_for('home'))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='HoverSpace | Login', form=form,current_user=current_user)

@app.route('/logout/')
def logout():
    session.pop('username', None)
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = USERS_COLLECTION.find_one( {'email': form.email.data} )
        if user:
            flash("You have already signed up from this email id", category='error')
        else:
            user = USERS_COLLECTION.find_one( {'_id': form.username.data} )
            if user:
                flash("That username has already been taken", category='error')
            else:
                user_obj = User(form.username.data, form.email.data, form.firstname.data,
                        form.lastname.data, form.password.data, db=True)
                session['username'] = form.username.data
                flash("SignUp successfull!", category='success')
                return redirect(url_for('home'))
    return render_template('signup.html', title='HoverSpace | Signup', form=form,current_user=current_user)

@app.route('/reading/', methods=['GET', 'POST'])
def reading():
    if request.method == 'POST':
        reading_date = request.form['reading_date']
        value = request.form['user_value']
        mood = request.form['user_mood']
        username = current_user.get_id()
        obj = Reading(username, reading_date, value, mood,db=True)
        return redirect(url_for('home'))
    return render_template('index.html')


@lm.user_loader
def load_user(username):
    u = USERS_COLLECTION.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
