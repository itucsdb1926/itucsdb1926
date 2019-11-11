from flask import Flask, render_template
from wtform_fields import *

#Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

@app.route("/", methods = ['GET', 'POST'])
def login():
	reg_form = RegistrationForm()
		if reg_form.validate_on_submit():
		return "Succesfully registered"
	return render_template("login_layout.html",form = reg_form)

if __name__== "__main__":
	app.run(debug=True)
