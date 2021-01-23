from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from form import RegisterForm, LoginForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] ='f00ee7583d29d7804578909a4ee52b96'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='uploader', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', {self.email})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

    def __repr__(self):
        return f"Post('{self.title}', {self.date_posted})"



@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if(form.validate_on_submit()):
        flash(f'Created account for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):
        if(form.email.data == 'vladi' and form.password.data == '1234'):
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login", form=form)

if __name__ == '__main__':
    app.run(debug=True)