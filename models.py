from flask import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for
from sqlalchemy import Column, ForeignKey, Integer, String

#=============================================
# MODELS FOR DB TABLES HERE
#=============================================

db = SQLAlchemy()

class User(db.Model, UserMixin):
		"""User Model"""
		__tablename__ = "users"
		id = db.Column(db.Integer, primary_key=True)
		username = db.Column(db.String(), unique=True, nullable=False)
		password = db.Column(db.String(), nullable=False)
		age = db.Column(db.Integer, nullable=False)
		weight = db.Column(db.Integer, nullable=False)
		height = db.Column(db.Integer, nullable=False)
		bmi = db.Column(db.Integer)
		blood_type = db.Column(db.String, nullable=False)
		family_doctor = db.Column(db.String, nullable=False)
		child = db.Column(db.Boolean, nullable=False)
		children = db.relationship('Children')
		appointments = db.relationship('AppointmentInfo')
		appointmenthistory = db.relationship('AppointmentHistory')
		vaccines = db.relationship("Vaccine")
		childrenvaccines = db.relationship("ChildrenVaccine")

		def __init__(self, **kwargs):
			super(User, self).__init__(**kwargs)

class Hospitals(db.Model):
	"""Hospital Model"""
	__tablename__ = "hospitals"
	id = db.Column(db.Integer, ForeignKey('adresses.id'), primary_key=True)
	name = db.Column(db.String(), unique=True, nullable=False)
	street = db.Column(db.String(), nullable=False)
	phone_number = db.Column(db.String(), nullable=False)
	type = db.Column(db.String(), nullable=False)
	clinic = db.Column(db.String(), nullable=False)
	polyclinic = db.Column(db.String())
	clinics = db.relationship("Clinics")
	doctors = db.relationship("Doctors")
	appointments = db.relationship("AppointmentInfo")
	appointmentshistory = db.relationship("AppointmentHistory")

	def __init__(self, **kwargs):
		super(Hospitals, self).__init__(**kwargs)

class Clinics(db.Model):
	"""Clinic Model"""
	__tablename__ = "clinics"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), unique=True, nullable=False)
	floor_number = db.Column(db.String(), unique=True, nullable=False)
	building_number = db.Column(db.String(), nullable=False)
	doctor_number = db.Column(db.Integer, nullable=False)
	asisstant = db.Column(db.String(), nullable=False)
	hospital = db.Column(db.String(), db.ForeignKey('hospitals.name'), nullable=False)
	doctors = db.relationship("Doctors")
	appointments = db.relationship("AppointmentInfo")
	appointmentshistory = db.relationship("AppointmentHistory")

	def __init__(self, **kwargs):
		super(Clinics, self).__init__(**kwargs)

class Doctors(db.Model):
	"""Doctors Model"""
	__tablename__ = "doctors"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(), unique=True, nullable=False)
	phone_number = db.Column(db.String(), unique=True, nullable=False)
	brans = db.Column(db.String(), nullable=False)
	room_no = db.Column(db.Integer, nullable=False)
	asisstant_name = db.Column(db.String(), nullable=False)
	hospital = db.Column(db.String(), db.ForeignKey('hospitals.name'), nullable=False)
	clinic = db.Column(db.String(), db.ForeignKey('clinics.name'), nullable=False)
	appointments = db.relationship("AppointmentInfo")
	appointmentshistory = db.relationship("AppointmentInfo")

	def __init__(self, **kwargs):
		super(Doctors, self).__init__(**kwargs)

class Adresses(db.Model):
	"""Andresses Model"""
	__tablename__ = "adresses"
	id = db.Column(db.Integer, primary_key=True)
	city = db.Column(db.String(), nullable=False)
	district = db.Column(db.String(), nullable=False)
	neighborhood = db.Column(db.String(), nullable=False)
	postal_code = db.Column(db.Integer)
	street = db.Column(db.String(), nullable=False)
	hospitals = db.relationship("Hospitals")

	def __init__(self, **kwargs):
		super(Adresses, self).__init__(**kwargs)

class AppointmentInfo(db.Model):
	"""Appointment Information Model"""
	__tablename__ = "appointment_info"
	id = db.Column(db.Integer, primary_key=True)
	doctor_name = db.Column(db.String(), db.ForeignKey('doctors.name'), unique=True, nullable=False)
	date = db.Column(db.Date, nullable=False)
	username = db.Column(db.String(), db.ForeignKey('users.username'), nullable=False)
	clinic = db.Column(db.String(), db.ForeignKey('clinics.name'), nullable=False)
	hospital_name = db.Column(db.String(), db.ForeignKey('hospitals.name'), nullable=False)
	def __init__(self, **kwargs):
		super(AppointmentInfo, self).__init__(**kwargs)

class AppointmentHistory(db.Model):
	"""Appointment History Model"""
	__tablename__ = "appointment_history"
	id = db.Column(db.Integer, primary_key=True)
	doctor_name = db.Column(db.String(), db.ForeignKey('doctors.name'), unique=True, nullable=False)
	date = db.Column(db.Date, nullable=False)
	city = db.Column(db.String(), nullable=False)
	status = db.Column(db.String(), nullable=False)
	username = db.Column(db.String(), db.ForeignKey('users.username'), nullable=False)
	clinic = db.Column(db.String(), db.ForeignKey('clinics.name'), nullable=False)
	hospital_name = db.Column(db.String(), db.ForeignKey('hospitals.name'), nullable=False)
	def __init__(self, **kwargs):
		super(AppointmentHistory, self).__init__(**kwargs)


class Children(db.Model):
	"""Children Model"""
	__tablename__ = "children"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	age = db.Column(db.Integer, nullable=False)
	weight = db.Column(db.Integer, nullable=False)
	height = db.Column(db.Integer, nullable=False)
	bmi = db.Column(db.Integer)
	blood_type = db.Column(db.String, nullable=False)
	parent = db.Column(db.String, db.ForeignKey('users.username'))
	childrenvaccines = db.relationship("ChildrenVaccine")
	def __init__(self, **kwargs):
		super(Children, self).__init__(**kwargs)

class ChildrenVaccine(db.Model):
	'''Children Vaccine Model'''
	__tablename__ = "children_vaccine"
	id = db.Column(db.Integer, primary_key=True)
	child_name = db.Column(db.String, db.ForeignKey('children.name'), nullable=False)
	name = db.Column(db.String,  nullable=False)
	date = db.Column(db.Date, nullable=False)
	place = db.Column(db.String)
	method = db.Column(db.String)
	dose = db.Column(db.String)
	parent = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
	def __init__(self, **kwargs):
		super(ChildrenVaccine, self).__init__(**kwargs)

class Vaccine(db.Model):
	'''Vaccine Model'''
	__tablename__ = "vaccine"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, db.ForeignKey('users.username'))
	name = db.Column(db.String, nullable=False)
	date = db.Column(db.Date, nullable=False)
	place = db.Column(db.String)
	method = db.Column(db.String)
	dose = db.Column(db.String)
	def __init__(self, **kwargs):
		super(Vaccine, self).__init__(**kwargs)

	with app.app_context():
		db.create_all()
