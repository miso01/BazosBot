from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators, IntegerField, MultipleFileField
import utils

sections = utils.fetch_bazos_sections()
price_select_values = ["Dohodou", "Ponúknite", "Zadarmo"]

field_is_required = "Toto pole je povinné."
title_min_length = "Názov musí obsahovať minimálne tri znaky."


class AdForm(FlaskForm):
    section = SelectField("section", choices=sections, validators=[validators.DataRequired(message=field_is_required)])
    category = SelectField("category", choices=[],
                           validators=[validators.DataRequired(message=field_is_required)])
    title = StringField("title", [validators.DataRequired(message=field_is_required),
                                  validators.Length(min=6, message=title_min_length)])
    text = StringField("text", validators=[validators.DataRequired(message=field_is_required)])
    price = IntegerField("price", validators=[validators.DataRequired(message=field_is_required)])
    price_select = SelectField("price_select",choices=price_select_values, validators=[validators.DataRequired(message=field_is_required)])
    zip_code = StringField("zip_code", [validators.DataRequired(message=field_is_required),
                                        validators.Length(min=6, message=title_min_length)])
    image = MultipleFileField("Pridať obrázky", validators=[validators.DataRequired(message=field_is_required)] )
    phone = StringField("phone", validators=[validators.DataRequired(message=field_is_required)])
    ad_password = PasswordField("ad_password", validators=[validators.DataRequired(message=field_is_required)])
