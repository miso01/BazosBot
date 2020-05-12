from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

field_is_required = "Toto pole je povinné."
email_incorrect_format = "Nesprávny formát e-mailu."
password_doesnt_match = "Hesla nie sú zhodné."
name_min_length = "Meno musí obsahovať minimálne tri znaky."
password_min_length = "Heslo musí obsahovať minimálne šesť znakov."


class RegisterForm(FlaskForm):
    username = StringField("username", validators=[validators.DataRequired(message=field_is_required),validators.Length(min=3, message=name_min_length)])
    email = StringField("email", validators=[validators.DataRequired(message=field_is_required),validators.Email(message=email_incorrect_format)])
    password = PasswordField("password", [validators.DataRequired(message=field_is_required),validators.Length(min=6, message=password_min_length)])
    confirm_password = PasswordField("confirm_password", validators=[validators.DataRequired(message=field_is_required),validators.EqualTo('confirm_password',message=password_doesnt_match)])


class LoginForm(FlaskForm):
    email = StringField("email", validators=[validators.DataRequired(message=field_is_required), validators.Email(message=email_incorrect_format)])
    password = PasswordField("password", validators=[validators.DataRequired(message=field_is_required), validators.Length(min=6, message=password_min_length)])
