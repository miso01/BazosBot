import string

from flask import flash
from bs4 import BeautifulSoup
import requests


def fetch_bazos_sections():
    page = requests.get('https://auto.bazos.sk/pridat-inzerat.php')
    soup = BeautifulSoup(page.text, 'html.parser')
    sections_data = soup.find_all("select", {"name": "rubriky"})
    sections_text = []
    sections_values = []
    for option in sections_data[0].find_all('option'):
        sections_text.append(option.text)
        sections_values.append(option["value"])
    return list(zip(sections_values, sections_text))


def fetch_bazos_categories(section):
    sct = section.translate(str.maketrans('', '', string.punctuation))
    sct.lower()
    page = requests.get('https://' + sct + '.bazos.sk/pridat-inzerat.php')
    soup = BeautifulSoup(page.text, 'html.parser')
    categories_data = soup.find_all("td", {"class": "listal"})
    categories_text = []
    categories_values = []

    for ctg in categories_data[0].find_all("a"):
        if "http" not in ctg["href"]:
            categories_text.append(ctg.text)
            categories_values.append(ctg["href"])
    return list(zip(categories_values, categories_text))


def get_category_text_from_category_section_value(section_value, category_value):
    fetched_categories = fetch_bazos_categories(section_value)

    category_list_tuple = [item for item in fetched_categories if item[0] == "/" + category_value + "/"]
    return category_list_tuple[0][1]


def flash_forms_errors(form):
    for fld, msg in form.errors.items():
        print("fild je " + str(fld) + " a msg je " + str(msg))
        flash(message=msg)
