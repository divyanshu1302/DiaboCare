from Diabocare.application import app, lm
import pymongo
import json
from flask import request, redirect, render_template, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from Diabocare.models import USERS_COLLECTION, READING_COLLECTION ,doctor_USERS_COLLECTION

from Diabocare.user import User
from Diabocare.doctor_user import Doctor_User
from Diabocare.reading import Reading

from Diabocare.forms import LoginForm, SignUpForm,doctor_LoginForm,doctor_SignUpForm  #, QuestionForm, AnswerForm
from bson.objectid import ObjectId

from datetime import date
from werkzeug.security import check_password_hash, generate_password_hash
from operator import itemgetter




@app.route('/')
@app.route('/home/', methods=['GET', 'POST'])
def home():
	if 'username' in session:
		a =  'You are logged in as ' + session['username']
		user_value = USERS_COLLECTION.find({'_id':current_user.get_id()})
		value = READING_COLLECTION.find({'postedBy': session['username']})
		print value
		# print Reading(value['value'])
		print type(value)

		reading_array = []
		reading_date_array = []


		for doc in value:
			print doc['value']
			print doc['reading_date']

			reading_array.append(doc['value'])
			reading_date_array.append(doc['reading_date'])

			print type(reading_array)
			# print type(doc)

		print reading_array
		print reading_date_array

	   


		k = zip(reading_array, reading_date_array)
		k = sorted(k, key=itemgetter(1))
		print k
		print type(k)
		uservalue = user_value[0]

		doctor_values = doctor_USERS_COLLECTION.find()
		special = []
		location =[]
		for i in doctor_values:
			print i['speciality'][0]
			special.append(i['speciality'][0])
			print i['city'][0]
			location.append(i['city'][0])

		# print uservalue['firstname'] 
		return render_template('index.html',a = a,current_user=current_user, k=k,user_value = uservalue, special=special, location=location)
	return render_template('home.html',current_user=current_user, form = LoginForm())


@login_required
@app.route('/userprofile/', methods=['GET', 'POST'])
def profile():
	user_value = USERS_COLLECTION.find({'_id':current_user.get_id()})
	uservalue = user_value[0]
	if request.method == 'POST':
		firstname = request.form['fname']
		lastname = request.form['lname']
		# uname = request.form['uname']
		# print uname
		dob = request.form['dob']
		addLine1 = request.form['addLine1']
		city = request.form['city']
		phne = request.form['phne']
		email = request.form['email']
		u_p = USERS_COLLECTION.find_one({ "_id": current_user.get_id() })
		up = u_p['password']
		p = USERS_COLLECTION.update({'_id': current_user.get_id()},{"$set":{'firstname':firstname,'lastname':lastname, 'email':email}})
		user = USERS_COLLECTION.update( { '_id': current_user.get_id()},{"$push":{'dob':dob,'addLine1' : addLine1,'city':city,'phne':phne}})
		return redirect(url_for('home'))
	return render_template('index.html',user_value = uservalue) #, title='HoverSpace | Profile', user=user)

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
	return render_template('login.html', title='Diabocare | Login', form=form,current_user=current_user)

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
	return render_template('signup.html', title='Diabocare | Signup', form=form,current_user=current_user)

@app.route('/reading/', methods=['GET', 'POST'])
def reading():
	user_value = USERS_COLLECTION.find({'_id':current_user.get_id()})
	uservalue = user_value[0]
	if request.method == 'POST':
		reading_date = request.form['reading_date']
		value = request.form['user_value']
		mood = request.form['user_mood']
		username = current_user.get_id()
		obj = Reading(username, reading_date, value, mood,db=True)
		return redirect(url_for('home'))
	return render_template('index.html',user_value = uservalue)


@lm.user_loader
def load_user(username):
	u = USERS_COLLECTION.find_one({"_id": username})
	if not u:
		return None
	return User(u['_id'])


@app.route('/datefilter/', methods=['GET', 'POST'])
def dateFilter():
	user_value = USERS_COLLECTION.find({'_id':current_user.get_id()})
	uservalue = user_value[0]
	if request.method == 'POST':
		from_date = request.form['reading_date_from']
		to_date = request.form['reading_date_to']

		print from_date
		print to_date

		print session['username']


		value = READING_COLLECTION.find({'postedBy': session['username'], 'reading_date': {'$gte': from_date, '$lte': to_date}})
		print value
		# print Reading(value['value'])
		print type(value)

		reading_array = []
		reading_date_array = []


		for doc in value:
			print doc['value']
			print doc['reading_date']

			reading_array.append(doc['value'])
			reading_date_array.append(doc['reading_date'])

			print type(reading_array)
			# print type(doc)

		print reading_array
		print reading_date_array

	   


		k = zip(reading_array, reading_date_array)

		print k
		print type(k)

		k = sorted(k, key=itemgetter(1))

		return render_template('index.html', k=k, reading_array=reading_array, reading_date_array=reading_date_array,user_value=user_value)

	return render_template('index.html',user_value=uservalue)

#Doctor................

@app.route('/logout/')
def doctorlogout():
	session.pop('username', None)
	logout_user()
	return redirect(url_for('doctorhome'))

@app.route('/doctorhome/', methods=['GET', 'POST'])
def doctorhome():
	if 'username' in session:
		user_value = doctor_USERS_COLLECTION.find({'_id':current_user.get_id()})
		uservalue = user_value[0]
		a =  'You are logged in as ' + session['username']
		return render_template('doctor_index.html',a = a,current_user=current_user,user_value =uservalue )
	return render_template('doctor_home.html',current_user=current_user, form = doctor_LoginForm())



@app.route('/doctor_signup/', methods=['GET', 'POST'])
def doctor_signup():
	form = doctor_SignUpForm()
	if request.method == 'POST' and form.validate_on_submit():
		user = doctor_USERS_COLLECTION.find_one( {'email': form.email.data} )
		if user:
			flash("You have already signed up from this email id", category='error')
		else:
			user = doctor_USERS_COLLECTION.find_one( {'_id': form.username.data} )
			if user:
				flash("That username has already been taken", category='error')
			else:
				user_obj = Doctor_User(form.username.data, form.email.data, form.firstname.data,
						form.lastname.data, form.password.data, db=True)
				session['username'] = form.username.data
				flash("SignUp successfull!", category='success')
				return redirect(url_for('doctorhome'))
	return render_template('doctor_signup.html', title='Diabocare | Signup', form=form,current_user=current_user)


@app.route('/doctor_login/', methods=['GET', 'POST'])
def doctor_login():
	form = doctor_LoginForm()
	if request.method == 'POST' and form.validate_on_submit():
		user = doctor_USERS_COLLECTION.find_one({ "_id": form.username.data })
		if user and Doctor_User.validate_login(user['password'], form.password.data):
			user_obj = Doctor_User(user['_id'])
			session['username'] = form.username.data
			login_user(user_obj, remember=True)
			flash("Logged in successfully!", category='success')
			return redirect(url_for('doctorhome'))
		flash("Wrong username or password!", category='error')
	return render_template('doctor_login.html', title='Diabocare | Login', form=form,current_user=current_user)

@app.route('/doctor_list/', methods=['GET', 'POST'])
def doctorlist():
	return render_template('doctor_list.html')

@login_required
@app.route('/doctorprofile/', methods=['GET', 'POST'])
def doctor_profile():
	user_value = doctor_USERS_COLLECTION.find({'_id':current_user.get_id()})
	uservalue = user_value[0]
	if request.method == 'POST':
		firstname = request.form['fname']
		lastname = request.form['lname']
		email = request.form['email']
		phne = request.form['phne']
		speciality = request.form['speciality']
		mSchool = request.form['mSchool']
		degrees = request.form['degrees']
		experience = request.form['experience']
		addLine1 = request.form['addLine1']
		city = request.form['city']
		message = request.form['message']
		# u_p = doctor_USERS_COLLECTION.find_one({ "_id": current_user.get_id() })
		# up = u_p['password']
		p = doctor_USERS_COLLECTION.update({'_id': current_user.get_id()},{"$set":{'firstname':firstname,'lastname':lastname, 'email':email }})
		user = doctor_USERS_COLLECTION.update( { '_id': current_user.get_id()},{"$push":{'addLine1' : addLine1,'city':city,'phne':phne,'speciality':speciality,'mSchool':mSchool,'degrees':degrees,'experience':experience,'addLine1':addLine1,'city':city,'message':message}})
		return redirect(url_for('doctorhome'))
	return render_template('doctor_index.html',user_value = uservalue) 


@app.route('/search/', methods=['GET', 'POST'])
def doctor_search():
	user_value = USERS_COLLECTION.find({'_id':current_user.get_id()})
	uservalue = user_value[0]

	if request.method == 'POST':
		doctor_special = request.form['speciality']
		doctor_location = request.form['location']

		print doctor_location
		print doctor_special

		answers = doctor_USERS_COLLECTION.find({'speciality': doctor_special, 'city': doctor_location })

		print answers

		firstname = []
		phone = []
		addLine1 = []

		for i in answers:
			print firstname.append(i['firstname'])
			print phone.append(i['phne'][0])
			print addLine1.append(i['addLine1'][0])

		print firstname
		print phone
		print addLine1

		l = zip(firstname, phone, addLine1)

		print l
		doctor_values = doctor_USERS_COLLECTION.find()
		special = []
		location =[]
		for i in doctor_values:
			print i['speciality'][0]
			special.append(i['speciality'][0])
			print i['city'][0]
			location.append(i['city'][0])

		value = READING_COLLECTION.find({'postedBy': session['username']})
		print value
		# print Reading(value['value'])
		print type(value)

		reading_array = []
		reading_date_array = []


		for doc in value:
			print doc['value']
			print doc['reading_date']

			reading_array.append(doc['value'])
			reading_date_array.append(doc['reading_date'])

			print type(reading_array)
			# print type(doc)

		print reading_array
		print reading_date_array

	   


		k = zip(reading_array, reading_date_array)
		k = sorted(k, key=itemgetter(1))
		print k
		print type(k)

		return render_template('index.html', user_value = uservalue, l=l, k=k, special=special, location=location)

	else:
		return redirect(url_for('home'))
