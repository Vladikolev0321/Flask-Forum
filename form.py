from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError #Email
#from flaskforum import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired()]) #should validate email?
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    '''def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if(user):
            raise ValidationError("That username is taken. Choose another one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if(email):
            raise ValidationError("That email is taken. Choose another one.")
            '''

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()]) #should validate email?
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    
    submit = SubmitField('Log in')

