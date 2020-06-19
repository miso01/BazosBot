import string

import requests
from bs4 import BeautifulSoup
import utils


class BazosHttp:
    #need to solve passing cookie to this class

    def __init__(self, cookie):

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

    def upload_image(self, base_url, path):
        """ We have to upload image first, request retruns image name,
            then we use image name in the post advertisement request """

        endpoint = "/upload.php"

        with open("static/" + path, 'rb') as f:
            f.seek(0)
            body = {"file[0]": f.read()}
            r = requests.post(base_url + endpoint, headers=self.headers, files=body)
            return r.text.replace("[", "").replace("]", "").replace("\"", "")

    def post_advertisements(self, advertisement, user, db):
        """ Posting advertisement to bazos"""
        endpoint = "/insert.php"

        ads = advertisement.query.all()

        for ad in ads:

            ad_owner = user.query.filter_by(id=ad.user_id).first()
            base_url = "https://" + ad.section_value + ".bazos.sk/"

            body = {
                "category": ad.category_value,
                "nadpis": ad.title,
                "popis": ad.text,
                "cena": ad.price,
                "cenavyber": ad.price_select,
                "lokalita": ad.zip_code,
                "jmeno": ad_owner.username,
                "telefoni": ad.phone,
                "maili": ad_owner.email,
                "heslobazar": ad.ad_password,
                "rterte": "gdfgdfga",
                "Submit": "Odoslať",
            }

            """ in order to send images to request we have to upload images separately first and
                then we have to send image name in request body """
            path_list = ad.image_paths.replace("{", "").replace("}", "").split(",")
            image_name_list = []
            for path in path_list:
                image_name = self.upload_image(base_url, path)
                image_name_list.append(image_name)

            body["files[]"] = image_name_list

            response = requests.post(base_url + endpoint, headers=self.headers, data=body)

            ad.bazos_id = self.get_advertisement_id(response.text, ad.title)
            db.session.commit()

    def delete_advertisements(self, advertisement):
        endpoint = "/deletei2.php"
        for ad in advertisement.query.all():
            base_url = "https://" + ad.section_value + ".bazos.sk/"

            body = {
                "heslobazar": ad.ad_password,
                "idad": ad.bazos_id,
                "administrace": "Zmazať"
            }

            requests.post(base_url + endpoint, headers=self.headers, data=body)

    def fetch_bazos_zip_code_suggestions(self, query):
        base_url = "https://auto.bazos.sk/"
        endpoint = "/suggestpscinsert.php?qnaspsc=" + query

        response = requests.get(base_url + endpoint, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find_all("td", {"class": "act"})
        zip_codes = []
        for zip_code in data:
            zip_codes.append(zip_code.text)
            print(zip_code.text)
        return zip_codes

    def fetch_bazos_categories(self, section):
        """Method for fetching categories based on selected category"""
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

    @staticmethod
    def get_advertisement_id(response_text, title):
        soup = BeautifulSoup(response_text, "html.parser")
        my_ads = soup.find_all("span", {"class": "nadpis"})
        for ad in my_ads:
            ad_url = ad.find_all("a")
            if title == ad_url[0].text:
                return utils.get_number_between_forward_slashes(ad_url[0]["href"])

    @staticmethod
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

    @staticmethod
    def get_bazos_price_options():
        return [(1, "Vyberte jednu z možností"),
                (2, "Dohodou"),
                (3, "Ponúknite"),
                (4, "Nerozhoduje"),
                (5, "V texte"),
                (6, "Zadarmo")]
