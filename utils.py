import string

from flask import flash
from bs4 import BeautifulSoup
import requests


def fetch_bazos_sections():
    page = requests.get('https://auto.bazos.sk/pridat-inzerat.php')
    soup = BeautifulSoup(page.text, 'html.parser')
    sections_data = soup.find_all("select", {"name": "rubriky"})
    print(sections_data)
    sections_text = []
    sections_values = []
    for option in sections_data[0].find_all('option'):
        sections_text.append(option.text)
        sections_values.append(option["value"])
    return list(zip(sections_values, sections_text))


def fetch_bazos_categories(section):
    sct = section.translate(str.maketrans('', '', string.punctuation))
    sct.lower()
    print(sct)

    page = requests.get('https://' + sct + '.bazos.sk/pridat-inzerat.php')
    soup = BeautifulSoup(page.text, 'html.parser')
    categories_data = soup.find_all("td", {"class": "listal"})
    print(categories_data)
    categories_text = []
    categories_values = []

    for ctg in categories_data[0].find_all("a"):
        if "http" not in ctg["href"]:
            categories_text.append(ctg.text)
            categories_values.append(ctg["href"])
            print(ctg.text)
    return list(zip(categories_values, categories_text))


def flash_forms_errors(form):
    for fld, msg in form.errors.items():
        flash(category=fld, message=msg)
