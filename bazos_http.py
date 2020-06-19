import string

import requests
from bs4 import BeautifulSoup
import utils


class BazosHttp:
    # need to solve passing cookie to this class

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

            ad.bazos_id = self.get_advertisement_id_after_advertisement_is_added(response.text, ad.title)
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

    @staticmethod
    def get_all_ads_ids(user_email):
        base_url = "https://www.bazos.sk"
        endpoint = "/moje-inzeraty.php?mail=" + user_email + "&Submit=Vyp%C3%ADsa%C5%A5+inzer%C3%A1ty"
        response = requests.get(base_url + endpoint)
        soup = BeautifulSoup(response.text, "html.parser")
        my_ads = soup.find_all("span", {"class": "nadpis"})
        ads_ids = []
        for ad in my_ads:
            ad_url = ad.find_all("a")
            ads_ids.append(utils.get_number_between_forward_slashes(ad_url[0]["href"]))
        return ads_ids

    @staticmethod
    def get_ad_data(ad_id):
        # search for advertisement with specified id
        base_url = "https://www.bazos.sk"
        endpoint = "/search.php?hledat=" + ad_id + "&Submit=H%C4%BEada%C5%A5&rubriky=www&hlokalita=&humkreis=25&cenaod=&cenado=&kitx=ano"
        response = requests.get(base_url + endpoint)
        soup = BeautifulSoup(response.text, "html.parser")
        my_ads = soup.find_all("span", {"class": "nadpis"})
        ads_ids = []
        for ad in my_ads:
            ad_url = ad.find_all("a")
            searched_ad_id = ads_ids.append(utils.get_number_between_forward_slashes(ad_url[0]["href"]))
            if searched_ad_id == ad:
                print("hrefko "+ ad_url[0]["href"])
        response
        base_url = "https://nabytok.bazos.sk/inzerat/112522940/macbook-air-2019-128gb-spacegray.php"
