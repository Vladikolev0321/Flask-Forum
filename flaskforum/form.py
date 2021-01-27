from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError #Email
from flaskforum.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired()]) #should validate email?
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    '''def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if(user is None):
            pass
        else:
            raise ValidationError("That username is taken. Choose another one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if(email is None):
            pass
        else:
            raise ValidationError("That email is taken. Choose another one.")
        '''

            

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) #should validate email?
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Log in')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    
class TopicForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	description = StringField('Description', validators=[DataRequired()])	
	submit = SubmitField('Create topic')







