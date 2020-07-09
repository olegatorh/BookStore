from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sing In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1)])
    email = StringField('Your mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    password1 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class BookStoreForm(FlaskForm):
    body = StringField('Comment', validators=[DataRequired(), Length(min=4, max=140)])
    submit = SubmitField('Submit Comment')
    wish_list = SubmitField('Add To Wish List')
    cart = SubmitField('Add To Cart')
