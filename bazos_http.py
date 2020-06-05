import re
import string

import requests
from bs4 import BeautifulSoup


class BazosHttp:

    def __init__(self,
                 cookie='_ga=GA1.2.1388617534.1590739305; __gfp_64b=9SqKXQEikg2hyptJMf.uA.H_qXz0i8qdzptYc0rBJor.C7; bkod=061S9KQLK8; bid=35707664; _gid=GA1.2.1410804962.1591029867; testcookie=ano; bmail=michal.svecko22%40gmail.com; btelefon=0948077165; bheslo=101478; bjmeno=Michal; fucking-eu-cookies=1; _gat_gtag_UA_58407_7=1'):

        self.headers = {
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'sk-SK,sk;q=0.9,cs;q=0.8,en-US;q=0.7,en;q=0.6',
            'cookie': cookie
        }

    def upload_image(self, base_url):
        """ We have to upload image first, request retruns image name,
            then we use image name in the post advertisement request """

        endpoint = "/upload.php"

        with open('static/uploads/7/d_4x3inb78a8gsz1qvqv4n84534456.jpeg', 'rb') as f:
            f.seek(0)
            body = {"file[0]": f.read()}
            r = requests.post(base_url + endpoint, headers=self.headers, files=body)
            return r.text.replace("[", "").replace("]", "").replace("\"", "")

    def post_advertisement(self, db, base_url):  # add advetisment
        """ Posting advertisement to bazos"""
        endpoint = "/insert.php"

        image_name = self.upload_image("https://elektro.bazos.sk/")

        body = {
            "category": "399",
            "nadpis": "Predám bluetooth slúchadlá QCY Q29",
            "popis": "Predám bluetooth slúchadlá QCY Q29.Komplet príslušenstvo, bez poškodenia, vyčistené.Používané len doma pri PC.V priemere tak hodinu týždenne.",
            "cena": "22",
            "cenavyber": "1",
            "lokalita": "01306",
            "jmeno": "Michal",
            "files[]": image_name,
            "telefoni": "0948077165",
            "maili": "michal.svecko22@gmail.com",
            "heslobazar": "101478",
            "rterte": "gdfgdfga",
            "Submit": "Odoslať",
        }

        r = requests.post(base_url + endpoint, headers=self.headers, data=body)

        print("text je ", r.text)
        print("content je ", r.content)

    def delete_advertisement(self, base_url):
        endpoint = "/deletei2.php"

        body = {
            "heslobazar": 101478,
            "idad": 112245352,
            "administrace": "Zmazať"
        }

        r = requests.post(base_url + endpoint, headers=self.headers, data=body)

    def get_advertisement_id(self, response_text, title):
        soup = BeautifulSoup(response_text, "html.parser")
        my_ads = soup.find_all("span", {"class": "nadpis"})
        for ad in my_ads:
            ad_url = ad.find_all("a")
            if title == ad_url[0].text:
                return self.get_number_between_fowardslashes(ad_url[0]["href"])

    def fetch_bazos_categories(self, section):
        """ method for fetching categories based on selected category"""
        sct = section.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
        sct.lower()
        page = requests.get('https://' + sct + '.bazos.sk/pridat-inzerat.php', headers=self.headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        categories_data = soup.find_all("select", {"id": "category"})
        categories_text = []
        categories_values = []
        for ctg in categories_data[0].find_all("option"):
            categories_text.append(ctg.text)
            categories_values.append(ctg["value"])
        return list(zip(categories_values, categories_text))

    def fetch_bazos_sections(self):
        page = requests.get('https://auto.bazos.sk/pridat-inzerat.php')
        soup = BeautifulSoup(page.text, 'html.parser')
        sections_data = soup.find_all("select", {"name": "rubriky"})
        sections_text = []
        sections_values = []
        for option in sections_data[0].find_all('option'):
            sections_text.append(option.text)
            sections_values.append(option["value"])
        return list(zip(sections_values, sections_text))


    def fetch_bazos_price_options(self):
        page = requests.get('https://auto.bazos.sk/pridat-inzerat.php')
        soup = BeautifulSoup(page.text, 'html.parser')
        sections_data = soup.find_all("select", {"name": "rubriky"})
        sections_text = []
        sections_values = []
        for option in sections_data[0].find_all('option'):
            sections_text.append(option.text)
            sections_values.append(option["value"])
        return list(zip(sections_values, sections_text))
