from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SelectField, validators, IntegerField, MultipleFileField
from wtforms.widgets import TextArea

from bazos_http import BazosHttp

sections = BazosHttp().fetch_bazos_sections()
price_select_values = [("dohodou", "Dohodou"), ("ponuknite","Ponúknite"), ("zadarmo", "Zadarmo")]#TODO tuple a bazos original values

field_is_required = "Toto pole je povinné."
title_min_length = "Názov musí obsahovať minimálne tri znaky."
zip_code_min_length = "PSČ musí obsahovať minimálne 5 znakov."


class AdForm(FlaskForm):
    section = SelectField("section", choices=sections, validators=[validators.DataRequired(message=field_is_required)])
    category = SelectField("category", choices=[],
                           validate_choice=False)
    title = StringField("title", [validators.DataRequired(message=field_is_required),
                                  validators.Length(min=3, message=title_min_length)])
    text = StringField("text", validators=[validators.DataRequired(message=field_is_required)], widget=TextArea())
    price = IntegerField("price", validators=[validators.DataRequired(message=field_is_required)])
    price_select = SelectField("price_select", choices=price_select_values,
                               validators=[validators.DataRequired(message=field_is_required)])
    zip_code = StringField("zip_code", [validators.DataRequired(message=field_is_required),
                                        validators.Length(min=5, max=5, message=zip_code_min_length)])
    image = MultipleFileField("Pridať obrázky", validators=[FileAllowed(['jpg', 'png'])])
    phone = StringField("phone", validators=[validators.DataRequired(message=field_is_required)])
    ad_password = PasswordField("ad_password", validators=[validators.DataRequired(message=field_is_required)])
