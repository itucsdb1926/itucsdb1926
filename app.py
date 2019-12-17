from flask import Flask, render_template, session, flash, request
from sqlalchemy import create_engine
from wtform_fields import *
from models import *
from flask_login import LoginManager, login_user, current_user, logout_user
from sqlalchemy.orm import sessionmaker



engine = create_engine('postgres://kwxcfhzwxzijhd:20b872dc2ac63fbc16cb904ce029beb2d64ce1a7aae26f5697c77a04e41ff1b4@ec2-176-34-184-174.eu-west-1.compute.amazonaws.com:5432/d7nb8bl3nfhaeb', echo=True)

#Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

#database configuration
app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://kwxcfhzwxzijhd:20b872dc2ac63fbc16cb904ce029beb2d64ce1a7aae26f5697c77a04e41ff1b4@ec2-176-34-184-174.eu-west-1.compute.amazonaws.com:5432/d7nb8bl3nfhaeb'
db = SQLAlchemy()

db.init_app(app)

# Initialize login manager
login = LoginManager(app)
login.init_app(app)

with app.app_context():
    db.create_all()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/rollback", methods=['GET'])
def rollback():
	db.session.rollback()
	return login()

@app.route("/")
def firstpage():
	form = LoginForm()
	return render_template("login_layout.html", form = form)

@app.route("/register", methods = ['GET', 'POST'])
def register():
	reg_form = RegistrationForm()
	if reg_form.validate_on_submit():
		username = reg_form.username.data
		password = reg_form.password.data

		# Hash password
		hashed_pswd = pbkdf2_sha256.hash(password)

		user = User(username=username,
					password= hashed_pswd,
					age = int(reg_form.age.data),
					weight = int(reg_form.weight.data),
					blood_type = reg_form.blood_type.data,
					height= int(reg_form.height.data),
					bmi=int(reg_form.bmi.data),
					family_doctor=reg_form.family_doctor.data,
					child=reg_form.child.data)

		db.session.add(user)
		db.session.commit()
		flash('Registered successfully! Please login..', 'success')
		log_form = LoginForm()
		return render_template("login_layout.html", form=log_form)
		
	return render_template("register_layout.html", form = reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
	log_form = LoginForm()
	if log_form.validate_on_submit():
		user_object = User.query.filter_by(username = log_form.username.data).first()
		session['username'] = log_form.username.data
		login_user(user_object)
		return render_template("index.html")

	return render_template("login_layout.html", form = log_form)

@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/appointment",  methods=['GET', 'POST'])
def appointment():
	app_form = AppointmentForm()
	if app_form.validate_on_submit():
		user_object = User.query.filter_by(username = app_form.username.data).first()
		if user_object:
			appointment = AppointmentInfo(username = app_form.username.data,
										  doctor_name = request.form.get('doctor_select'),
										  date = app_form.date.data,
										  hospital_name = request.form.get('hospital_select'),
										  clinic = request.form.get('clinic_select'))
			db.session.add(appointment)
			db.session.commit()
			flash('Booked your appointment successfully!')

	return render_template("appointment.html", form = app_form)

@app.route("/logout")
def logout():
	session['logged_in'] = False
	del session['username']
	log_form = LoginForm()
	return render_template("login_layout.html", form=log_form)

@app.route("/info")
def info():
	rows = AppointmentHistory.query.filter_by(username=session['username']).all()
	return render_template("Appointment_Information.html", rows = rows)

@app.route("/history")
def history():
	rows = User.query.filter_by(username=session['username']).all()
	return render_template("Appointment_History.html", rows = rows)

@app.route("/vaccine", methods = ['GET', 'POST'])
def vaccine():
	rows = Vaccine.query.filter_by(username=session['username']).all()
	return render_template("vaccine.html", rows=rows)

@app.route("/addvaccine", methods = ['GET', 'POST'])
def addvaccine():
	vaccine_form = VaccineForm()
	if request.form:
		vaccine = Vaccine(username = session['username'],
						name=request.form.get("name"),
						  doctor=request.form.get("doctor"),
						  date = request.form.get("date"),
						  place = request.form.get("place"),
						   method = request.form.get("method"),
						  dose = request.form.get("dose"))
		db.session.add(vaccine)
		db.session.commit()
	return render_template("addvaccine.html", form = vaccine_form)

@app.route("/childrenvaccine", methods = ['GET', 'POST'])
def childrenvaccine():
	rows = ChildrenVaccine.query.filter_by(parent = session['username']).all()
	return render_template("childrenvaccine.html", rows=rows)

@app.route("/addchildrenvaccine", methods = ['GET', 'POST'])
def addchildrenvaccine():
	childrenvaccine_form = ChildrenVaccineForm
	if request.form:
		cvaccine = ChildrenVaccine(child_name = request.form.get("child_name"),
									name = request.form.get("name"),
										  place = request.form.get("place"),
										  dose = request.form.get("dose"),
										  method = request.form.get("method"),
										  date = request.form.get("date"),
								   parent = session['username'])
		db.session.add(cvaccine)
		db.session.commit()
	return render_template("addchildrenvaccine.html", form=childrenvaccine_form)

@app.route("/children", methods = ['GET', 'POST'])
def children():
	rows = Children.query.filter_by(parent=session['username']).all()
	return render_template("children.html", rows= rows)

@app.route("/addchildren", methods = ['GET', 'POST'])
def addchildren():
	children_form = ChildrenForm()
	if request.form:
		children = Children(name=request.form.get("name"),
							height=request.form.get("height"),
							weight = request.form.get("weight"),
							age = request.form.get("age"),
							bmi = request.form.get("bmi"),
							blood_type = request.form.get("blood_type"),
							parent = session['username'])
		db.session.add(children)
		db.session.commit()
	return render_template("addchild.html", form=children_form)


if __name__== "__main__":
	app.run(debug=True)
 
