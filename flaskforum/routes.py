from operator import pos
from flask import render_template, url_for, flash, redirect, request
from flaskforum import app
from flaskforum.form import RegisterForm, LoginForm, PostForm, TopicForm
from flaskforum.models import User, Post, Topic
from flaskforum import bcrypt
from flaskforum import db
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
    topics = Topic.query.all()
    return render_template('home.html', topics=topics)

@app.route("/register", methods=['GET','POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = RegisterForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()
        if(user):
            flash('That username is taken. Choose another one.', 'danger')
            return redirect(url_for('register'))
        user2 = User.query.filter_by(email=form.email.data).first()
        if(user2):
            flash('That email is taken. Choose another one.', 'danger')
            return redirect(url_for('register'))

        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Created account for {form.username.data}. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    form = LoginForm()
    if(form.validate_on_submit()):
        #if(form.email.data == 'vladi' and form.password.data == '1234'):
        user = User.query.filter_by(username=form.username.data).first()
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/logged_in")
@login_required
def logged_in():
    return render_template('logged_in.html', title="My account")

@app.route("/make_topic", methods=['GET', 'POST'])
@login_required
def make_topic():
    form = TopicForm()
    if(form.validate_on_submit()):
        topic = Topic(title=form.title.data, description=form.description.data)
        db.session.add(topic)
        db.session.commit()
        flash('Your topic has been created', 'success')
        return redirect(url_for('home'))
    return render_template('make_post.html', title='New post', form=form)

@app.route("/topic/<int:topic_id>", methods=['GET', 'POST'])
def topic(topic_id):
    topic = Topic.query.get(topic_id)
    return render_template('topic.html', title=topic.title, topic=topic)

@app.route("/not_finished")
def not_finished():
    return render_template('notfinished.html', title="Not Finished")
