from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import InputRequired, Length, EqualTo


class RegistrationForm(FlaskForm):	
	username = StringField('username', validators=[InputRequired(message="Username required")])
	password = PasswordField('password', validators=[InputRequired(message="Password required")])
	confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])
	submit_button = SubmitField('Login')
