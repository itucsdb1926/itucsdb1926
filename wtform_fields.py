from flask_sqlalchemy import Model
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,DateField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User, Hospitals, Clinics, Children, ChildrenVaccine, Vaccine, AppointmentHistory, AppointmentInfo, Doctors
from passlib.hash import pbkdf2_sha256
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for
from sqlalchemy import Column, ForeignKey, Integer, String


db = SQLAlchemy()

def validate_username(self, username):
	user_object = User.query.filter_by(username=username.data).first()
	if user_object:
		raise ValidationError("Username already exists. Select a different username.")

class RegistrationForm(FlaskForm):	
	username = StringField('username', validators=[InputRequired(message="Username required"), validate_username])
	password = PasswordField('password', validators=[InputRequired(message="Password required")])
	confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])
	age = StringField('age', validators=[InputRequired(message="Age required")])
	weight = StringField('weight', validators=[InputRequired(message="Weight required")])
	height = StringField('height', validators=[InputRequired(message="Height required")])
	bmi = StringField('bmi')
	blood_type = StringField('blood_type', validators=[InputRequired(message="Blood type required")])
	family_doctor = StringField('family_doctor', validators=[InputRequired(message="Family doctor required")])
	child = BooleanField('child', validators=[InputRequired(message="Child information required")])
	submit_button = SubmitField('Register')


def invalid_credentials(form, field):
    """ Username and password checker """

    password = field.data
    username = form.username.data

    # Check username is invalid
    user_data = User.query.filter_by(username=username).first()
    if user_data is None:
        raise ValidationError("Username or password is incorrect")

    # Check password in invalid
    elif not pbkdf2_sha256.verify(password, user_data.password):
        raise ValidationError("Username or password is incorrect")

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(message="Username required")])
	password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])
	submit_button = SubmitField('Login')

def get_hospital_names():
	""" databasedeki hospitals tablosundan name sütunu çekilip hospital_names arrayine atılacak"""

	hospital_names = Hospitals.query.with_entities(Hospitals.name).all()
	hospitals = Hospitals.query.order_by(Hospitals.name).all()
	for hospital in hospitals:
		hospital_names.append(hospital.name)

	return hospital_names

def get_doctor_names():
	doctor_names = Doctors.query.with_entities(Doctors.name).all()
	doctors = Doctors.query.order_by(Doctors.name).all()
	for doctor in doctors:
		doctor_names.append(doctor.name)
	return doctor_names

def get_clinic_names():
	clinic_names = Clinics.query.with_entities(Clinics.name).all()
	clinics = Clinics.query.order_by(Clinics.name).all()
	for clinic in clinics:
		clinic_names.append(clinic.name)
	return clinic_names

class AppointmentForm(FlaskForm):
	""" Randevu alınırken kullanılacak form """
	username = StringField('username', validators=[InputRequired(message="Username required")])
	hospital_name = SelectField('hospital_name', choices = ['get_hospital_names'])
	clinic = SelectField('clinic', choices =  ['get_clinic_names'] )
	doctor_name = SelectField('doctor_name', choices = ['get_doctor_names'] )
	date = DateField('date' , validators=[InputRequired(message="Please Select an Appointment Date")])
	submit_button = SubmitField('Book An Appointment')

class ChildrenForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(message="Child name required")])
	age = StringField('age', validators=[InputRequired(message="Age required")])
	weight = StringField('weight', validators=[InputRequired(message="Weight required")])
	height = StringField('height', validators=[InputRequired(message="Height required")])
	bmi = StringField('bmi')
	blood_type = StringField('blood_type', validators=[InputRequired(message="Blood type required")])
	submit_button = SubmitField('Add')

class VaccineForm(FlaskForm):
	name = StringField('name', validators=[InputRequired(message="Vaccine name required")])
	date = StringField('date', validators=[InputRequired(message="Date required")])
	place = StringField('place')
	dose = StringField('dose')
	method = StringField('method')
	doctor = StringField('doctor')
	submit_button = SubmitField('Add')

class ChildrenVaccineForm(FlaskForm):
	child_name = StringField('child name', validators=[InputRequired(message="child name required")])
	name = StringField('name', validators=[InputRequired(message="Vaccine name required")])
	date = StringField('date', validators=[InputRequired(message="Date required")])
	place = StringField('place')
	dose = StringField('dose')
	method = StringField('method')
	doctor = StringField('doctor')
	submit_button = SubmitField('Add')