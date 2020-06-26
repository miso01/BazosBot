import itertools
from datetime import datetime

import flask_login
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user

import utils
from bazos_http import BazosHttp
from models import User, db, Advertisement

ads = Blueprint('ads', __name__)


@ads.route('/ads')
@flask_login.login_required
def advertisements():
    user = User.query.filter_by(id=current_user.get_id()).first()
    user_ads = Advertisement.query.join(User).filter(Advertisement.id == user.id)
    user_ads_html = ""

    bazos_http = BazosHttp(
        "_ga=GA1.2.1097115696.1591092093; _gid=GA1.2.578207826.1591092093; bid=35797869; bkod=273WXWMGFP; testcookie=ano; __gfp_64b=k78R.IcLOGgD2nSd5M4F4fgtq4lw0.el4mlV8DOCzMb.37")

    base_url = "https://www.bazos.sk"
    endpoint = "/moje-inzeraty.php?mail=" + user.email + "&Submit=Vyp%C3%ADsa%C5%A5+inzer%C3%A1ty"
    response = requests.get(base_url + endpoint)

    soup = BeautifulSoup(response.text, "html.parser")
    my_ads_titles = soup.find_all("span", {"class": "nadpis"})
    my_ads = soup.find_all("span", {"class": "vypis"})
    for i in range(len(my_ads_titles)):
        ad_url = my_ads_titles[i].find_all("a")
        id = utils.get_number_between_forward_slashes(ad_url[0]["href"])
        for ad in user_ads:
            if ad.ad_id == id:
                user_ads_html += str(my_ads[i])

    return render_template('advertisements.html', ads=user_ads_html)


@ads.route('/ads/add', methods=["POST", "GET"])
@flask_login.login_required
def add_advertisement():
    return render_template('add_ad.html')


@ads.route('/save_bazos_cookie/<cookie>')
@flask_login.login_required
def save_bazos_cookie(cookie):
    user = User.query.filter_by(id=current_user.get_id()).first()
    print("cookie je " + cookie)
    user.cookie = cookie
    db.session.commit()
    return ""


@ads.route('/save_ads_ids', methods=["POST"])
def ed():
    user = User.query.filter_by(id=current_user.get_id()).first()
    ads_ids = request.form.getlist("ads_ids[]")
    intervals = request.form.getlist("intervals[]")

    print("ads_ids lenght je " + str(len(ads_ids)))
    print("intervals  lenght je " + str(len(intervals)))
    if len(ads_ids) == 0:
        ads_ids = BazosHttp(
            "_ga=GA1.2.1097115696.1591092093; _gid=GA1.2.578207826.1591092093; bid=35797869; bkod=273WXWMGFP; testcookie=ano; __gfp_64b=k78R.IcLOGgD2nSd5M4F4fgtq4lw0.el4mlV8DOCzMb.37").get_all_ads_ids(
            user.email)
        # single interval for every advertisement
        ads = zip(ads_ids, itertools.repeat(intervals[0]))
    else:
        ads = zip(ads_ids, intervals)

    for ad_id, interval in ads:
        print("for lopp toto je idecko " + ad_id)
        print("for lopp toto je interval " + interval)
        user.ads.append(Advertisement(ad_id=ad_id, interval=interval, refresh_date=datetime.utcnow()))

    db.session.add(user)
    db.session.commit()
    return "SUCCESS"


@ads.route('/save_profile', methods=["POST"])
def save_profile():
    user = User.query.filter_by(id=current_user.get_id()).first()
    cookie = request.form.get("cookie")
    ad_password = request.form.get("ad_password")
    user.cookie = cookie
    user.ad_password = ad_password
    db.session.add(user)
    db.session.commit()
    return "SUCCESS"
