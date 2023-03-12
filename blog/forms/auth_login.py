from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class UserLoginForm(FlaskForm):
    email = StringField('E-mail', [validators.DataRequired(), validators.Email(message='Ошибка в email')])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')
