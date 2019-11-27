from flask import Flask, render_template
from wtform_fields import *
from models import *

#Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

#database configuration

app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://kwxcfhzwxzijhd:20b872dc2ac63fbc16cb904ce029beb2d64ce1a7aae26f5697c77a04e41ff1b4@ec2-176-34-184-174.eu-west-1.compute.amazonaws.com:5432/d7nb8bl3nfhaeb'
db = SQLAlchemy(app)


@app.route("/", methods = ['GET', 'POST'])
def login():
	reg_form = RegistrationForm()
	if reg_form.validate_on_submit():
		username = reg_form.username.data
		password = reg_form.password.data
		
		#check username exists
		user_object = User.query.filter_by(username = username).first()
		if user_object:
			return "Someone else has taken this username!"
		
		user = User(username = username, password = password)
		db.session.add(user)
		db.session.commit()
		return "Inserted into DB!"
		
	return render_template("login_layout.html",form = reg_form)

if __name__== "__main__":
	app.run(debug=True)
 
