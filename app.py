from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import NewUserForm
from flask_bcrypt import Bcrypt
from flask_wtf import CsrfProtect

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/flask_user_template'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'shhhh'

CsrfProtect(app)

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.Text, nullable = False)
	password = db.Column(db.Text, nullable = False)

	def __init__(self, username, password):
		self.username = username
		self.password = bcrypt.generate_password_hash(password).decode('utf-8')


@app.route('/')
def root():
	return render_template('index.html')


@app.route('/users')
def index_user():
	users = User.query.all()
	return render_template('users/index.html', users=users)

@app.route('/users', methods=['POST'])
def create_user():
	form = NewUserForm()
	import pdb; pdb.set_trace()
	if form.validate_on_submit():
		import pdb; pdb.set_trace()
		new_user = User(form.username.data, form.password.data)
		db.session.add(new_user)
		db.session.commit()
		flash('You Just Created A User!')
	return redirect(url_for('index_user'))

@app.route('/users/new')
def new_user():
	form = NewUserForm()
	return render_template('users/new.html', form = form)

if __name__ == '__main__':
	app.run(debug = True, port=3000)