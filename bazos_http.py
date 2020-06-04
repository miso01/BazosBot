class BazosHttp:


    def __init__(self, cookie, ):
        headers = {
            'authority': 'elektro.bazos.sk',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'origin': 'https://elektro.bazos.sk',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://elektro.bazos.sk/pridat-inzerat.php',
            'accept-language': 'sk-SK,sk;q=0.9,cs;q=0.8,en-US;q=0.7,en;q=0.6',
            'cookie': '_ga=GA1.2.1388617534.1590739305; __gfp_64b=9SqKXQEikg2hyptJMf.uA.H_qXz0i8qdzptYc0rBJor.C7; bkod=061S9KQLK8; bid=35707664; _gid=GA1.2.1410804962.1591029867; testcookie=ano; bmail=michal.svecko22%40gmail.com; btelefon=0948077165; bheslo=101478; bjmeno=Michal; fucking-eu-cookies=1; _gat_gtag_UA_58407_7=1'
        }