from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    username = StringField('Username(min=6, max=35)', [DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address(min=6, max=35)', [DataRequired(), Email(), Length(min=6, max=35)])
    firstname = TextField("First name", [DataRequired()])
    lastname = TextField("Last name", [DataRequired()])
    password = PasswordField('Password(min=6)', [DataRequired(), Length(min=6)])


class doctor_LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class doctor_SignUpForm(FlaskForm):
    username = StringField('Username(min=6, max=35)', [DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address(min=6, max=35)', [DataRequired(), Email(), Length(min=6, max=35)])
    firstname = TextField("First name", [DataRequired()])
    lastname = TextField("Last name", [DataRequired()])
    password = PasswordField('Password(min=6)', [DataRequired(), Length(min=6)])


