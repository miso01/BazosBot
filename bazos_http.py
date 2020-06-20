import string
import re

import requests
from bs4 import BeautifulSoup
import utils


def get_images_url_from_ad_detail(soup):
    images_urls = []
    carousel = soup.find_all("div", {"class": "carousel-cell"})
    for image in carousel:
        img_element = image.find_all("img", {"class": "carousel-cell-image"})
        img_url = img_element[0]["data-flickity-lazyload"]
        images_urls.append(img_url)
    return images_urls


def get_description_from_ad_detail(soup):
    description_div = soup.find_all("div", {"class": "popis"})
    return description_div[0].text


def get_title_from_ad_detail(soup):
    title_element = soup.find_all("title")
    return title_element[0].text

def get_price_from_ad_detail(soup):
    td_elements = soup.find_all("td", {"colspan": "2"})
    last_td = td_elements[len(td_elements) -1]
    price = last_td.find_all("b")[0].text
    formatted_price = price.replace("€", "").strip()
    return formatted_price


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

    def get_ad_data(self, ad_id):
        # this data we need for uploading advertisement to bazos
        ad_images_urls = []
        ad_description = ""
        ad_title = ""
        ad_phone = ""
        ad_price = ""
        # search for advertisement with specified id
        base_url = "https://www.bazos.sk"
        endpoint = "/search.php?hledat=" + ad_id + "&Submit=H%C4%BEada%C5%A5&rubriky=www&hlokalita=&humkreis=25&cenaod=&cenado=&kitx=ano"
        response = requests.get(base_url + endpoint)
        soup = BeautifulSoup(response.text, "html.parser")
        my_ads = soup.find_all("span", {"class": "nadpis"})
        for ad in my_ads:
            ad_url = ad.find_all("a")
            searched_ad_id = utils.get_number_between_forward_slashes(ad_url[0]["href"])
            if searched_ad_id == ad_id:
                ad_detail_url = ad_url[0]["href"]
                print("ad detail url" + ad_detail_url)
                response = requests.get(ad_detail_url)
                print(response.text)

                soup = BeautifulSoup(response.text, "html.parser")
                ad_images_urls = get_images_url_from_ad_detail(soup)
                ad_description = get_description_from_ad_detail(soup)
                ad_title = get_title_from_ad_detail(soup)
                ad_phone = self.get_phone_from_ad_detail(soup)
                ad_price = get_price_from_ad_detail(soup)


    def get_phone_from_ad_detail(self, soup):
        phone_detail_url = soup.find_all("span", {"class": "teldetail"})
        onclick = phone_detail_url[0]["onclick"]
        result = re.search("odeslatrequest\('(.*)'\);", onclick)
        phone_endpoint = result.group(1)
        base_url = "https://auto.bazos.sk"
        response = requests.get(base_url + phone_endpoint, headers=self.headers)
        print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        phone_span = soup.find_all("span", {"class": "teldetail"})
        phone = phone_span[0].find_all("a")[0].text
        return phone


