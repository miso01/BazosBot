from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators, IntegerField
from bs4 import BeautifulSoup
import requests

page = requests.get('https://auto.bazos.sk/pridat-inzerat.php')

soup = BeautifulSoup(page.text, 'html.parser')

sections_data = soup.find_all("select", {"name": "rubriky"})

categories_data = soup.find_all("td", {"class": "listal"})

print(categories_data)

categories = []

for ctg in categories_data[0].find_all("a"):
    if not "http" in ctg["href"]:
        categories.append(ctg.text)

sections = []

for option in sections_data[0].find_all('option'):
    value = option.text  # alebo value
    sections.append(value)
    print(value)

# print(soup)


# print(categ)


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
    zip_code = StringField("zip_code", [validators.DataRequired(message=field_is_required),
                                        validators.Length(min=6, message=title_min_length)])
    phone = StringField("phone", validators=[validators.DataRequired(message=field_is_required)])
    ad_password = PasswordField("ad_password", validators=[validators.DataRequired(message=field_is_required)])
