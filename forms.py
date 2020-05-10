from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField


class RegisterForm(FlaskForm):
    username = StringField("username")
    email = StringField("email")
    password = PasswordField("password")
    confirm_password = PasswordField("confirm_password")


class LoginForm(FlaskForm):
    email = StringField("email", )
    password = PasswordField("password")


