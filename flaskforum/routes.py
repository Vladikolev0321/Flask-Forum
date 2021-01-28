from operator import pos
from flask import render_template, url_for, flash, redirect, request, abort
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
    return render_template('make_topic.html', title='New Topic', form=form)

@app.route("/topic/<int:topic_id>", methods=['GET', 'POST'])
def topic(topic_id):
    topic = Topic.query.get(topic_id)
    #posts = Post.query.all()
    #get all posts by topic id here not in the html
    return render_template('topic.html', title=topic.title, topic=topic, posts=topic.posts)

@app.route("/not_finished")
def not_finished():
    return render_template('notfinished.html', title="Not Finished")

@app.route("/topic/<int:topic_id>/make_post", methods=['GET', 'POST'])
@login_required
def make_post(topic_id):
    form = PostForm()
    if(form.validate_on_submit()):
        curr_topic = Topic.query.get(topic_id)
        post = Post(title=form.title.data, content=form.content.data, uploader=current_user, current_topic=curr_topic)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('topic', topic_id=topic_id))
    return render_template('make_post.html', title='New Post', form=form, legend="New Post")
    
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.uploader != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('make_post.html', title='Update Post', form=form, legend="Update Post") 


@app.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.uploader != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
    
@app.route("/about")
def about():
    return render_template('about.html', title="About page")
    
















