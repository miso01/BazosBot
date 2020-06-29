import re
from datetime import datetime

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

    def upload_image(self, base_url, image_url):
        """ We have to upload image first, request retruns image name,
            then we use image name in the post advertisement request """

        endpoint = "/upload.php"
        response = requests.get(image_url)
        body = {"file[0]": response.content}
        response = requests.post(base_url + endpoint, headers=self.headers, files=body)
        return response.text.replace("[", "").replace("]", "").replace("\"", "")

    def post_advertisement(self, ad, user, advertisement, db):
        """ Posting advertisement to bazos"""
        endpoint = "/insert.php"

        try:
            ad_detail = self.get_ad_detail(ad.ad_id)
            soup = BeautifulSoup(ad_detail, "html.parser")
        except TypeError:
            db.session.delete(ad)
            db.session.commit()
            return

        ad_images_urls = self.get_images_url_from_ad_detail(soup)
        ad_description = self.get_description_from_ad_detail(soup)
        ad_title = self.get_title_from_ad_detail(soup)
        ad_phone = self.get_phone_from_ad_detail(soup)
        ad_price = self.get_price_from_ad_detail(soup)
        ad_category = self.__get_category_from_ad_detail(soup)
        ad_section = self.get_section_from_ad_detail(soup)
        ad_zip_code = self.get_zip_code_from_ad_detail(soup)

        base_url = "https://" + ad_section + ".bazos.sk/"

        body = {
            "category": ad_category,
            "nadpis": ad_title,
            "popis": ad_description,
            "cena": ad_price,
            "cenavyber": self.choose_cenavyber(ad_price),
            "lokalita": ad_zip_code,
            "jmeno": user.username,
            "telefoni": ad_phone,
            "maili": user.email,
            "heslobazar": user.ad_password,
            "rterte": "gdfgdfga",
            "Submit": "Odoslať",
        }

        """ in order to send images to request we have to upload images separately first and
            then we have to send image name in request body """

        image_name_list = []
        for image_url in ad_images_urls:
            image_name = self.upload_image(base_url, image_url)
            image_name_list.append(image_name)

        body["files[]"] = image_name_list

        response = requests.post(base_url + endpoint, headers=self.headers, data=body)
        if response.status_code == 200:
            self.delete_advertisement(user, ad, ad_section)
            new_ad_id = self.get_ad_id_from_title(user.email, ad_title)
            db.session.delete(ad)
            if new_ad_id:
                user.ads.append(advertisement(ad_id=new_ad_id, interval=ad.interval, refresh_date=datetime.utcnow()))
            db.session.commit()

    def delete_advertisement(self, user, ad, section):
        endpoint = "/deletei2.php"

        base_url = "https://" + section + ".bazos.sk/"

        body = {
            "heslobazar": user.ad_password,
            "idad": ad.ad_id,
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
    def get_ad_id_from_title(user_email, title):
        base_url = "https://www.bazos.sk"
        endpoint = "/moje-inzeraty.php?mail=" + user_email + "&Submit=Vyp%C3%ADsa%C5%A5+inzer%C3%A1ty"
        response = requests.get(base_url + endpoint)
        soup = BeautifulSoup(response.text, "html.parser")
        my_ads = soup.find_all("span", {"class": "nadpis"})
        for ad in my_ads:
            ad_url = ad.find_all("a")
            if title == ad_url[0].text:
                return utils.get_number_between_forward_slashes(ad_url[0]["href"])
        return None

    @staticmethod
    def get_ad_detail(ad_id):
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
                response = requests.get(ad_detail_url)
                return response.text

    def get_phone_from_ad_detail(self, soup):
        phone_detail_url = soup.find_all("span", {"class": "teldetail"})
        onclick = phone_detail_url[0]["onclick"]
        result = re.search("odeslatrequest\('(.*)'\);", onclick)
        phone_endpoint = result.group(1)
        base_url = "https://auto.bazos.sk"
        response = requests.get(base_url + phone_endpoint, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        phone_span = soup.find_all("span", {"class": "teldetail"})
        phone = phone_span[0].find_all("a")[0].text
        return phone

    @staticmethod
    def get_my_ads(user_ads, user_email):
        my_ads_html = []
        my_ads = []
        base_url = "https://www.bazos.sk"
        endpoint = "/moje-inzeraty.php?mail=" + user_email + "&Submit=Vyp%C3%ADsa%C5%A5+inzer%C3%A1ty"
        response = requests.get(base_url + endpoint)
        soup = BeautifulSoup(response.text, "html.parser")
        all_ads_titles = soup.find_all("span", {"class": "nadpis"})
        all_ads = soup.find_all("span", {"class": "vypis"})
        for i in range(len(all_ads_titles)):
            ad_url = all_ads_titles[i].find_all("a")
            id = utils.get_number_between_forward_slashes(ad_url[0]["href"])
            for ad in user_ads:
                if ad.ad_id == id:
                    my_ads.append(ad)
                    my_ads_html.append(str(all_ads[i]))

        data = zip(my_ads, my_ads_html)
        return data

    @staticmethod
    def get_images_url_from_ad_detail(soup):
        images_urls = []
        carousel = soup.find_all("div", {"class": "carousel-cell"})
        for image in carousel:
            img_element = image.find_all("img", {"class": "carousel-cell-image"})
            img_url = img_element[0]["data-flickity-lazyload"]
            images_urls.append(img_url)
        return images_urls

    @staticmethod
    def get_description_from_ad_detail(soup):
        description_div = soup.find_all("div", {"class": "popis"})
        return description_div[0].text

    @staticmethod
    def get_title_from_ad_detail(soup):
        title_element = soup.find_all("title")
        return title_element[0].text

    @staticmethod
    def get_price_from_ad_detail(soup):
        td_elements = soup.find_all("td", {"colspan": "2"})
        last_td = td_elements[len(td_elements) - 1]
        price = last_td.find_all("b")[0].text
        formatted_price = price.replace("€", "").strip()
        return formatted_price

    @staticmethod
    def __get_category_from_ad_detail(soup):
        link_element = soup.find_all("link", {"rel": "alternate"})
        link_href = link_element[0]["href"]
        result = re.search("cat=(.*)", link_href)
        category_id = result.group(1)
        return category_id

    @staticmethod
    def get_zip_code_from_ad_detail(soup):
        a_element = soup.find_all("a", {"title": "Približná lokalita"})
        location = a_element[0].text
        zip_code = location[0: 6].replace(" ", "")
        return zip_code

    @staticmethod
    def get_section_from_ad_detail(soup):
        div_element = soup.find_all("div", {"class": "drobky"})
        a_elements = div_element[0].find_all("a")
        result = re.search('//(.*).baz', a_elements[1]["href"])
        section = result.group(1)
        return section

    @staticmethod
    def choose_cenavyber(price):
        if price == "Dohodou":
            return 2
        elif price == "Ponúknite":
            return 3
        elif price == "Nerozhoduje":
            return 4
        elif price == "V texte":
            return 5
        elif price == "Zadarmo":
            return 6
        else:
            return 1
