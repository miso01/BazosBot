import requests


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

    def post_advertisement(self, base_url):# add advetisment
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
        r
