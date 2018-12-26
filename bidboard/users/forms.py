from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, PasswordField, SubmitField


class SignupForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    company_name = StringField('Company Name')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
