from datetime import datetime

import flask_login
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user

import utils
from bazos_http import BazosHttp
from models import User, db

ads = Blueprint('ads', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@ads.route('/ads')
@flask_login.login_required
def advertisements():
    return render_template('advertisements.html')


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
    if len(ads_ids) == 0:
        ads_ids = BazosHttp(
        "_ga=GA1.2.1097115696.1591092093; _gid=GA1.2.578207826.1591092093; bid=35797869; bkod=273WXWMGFP; testcookie=ano; __gfp_64b=k78R.IcLOGgD2nSd5M4F4fgtq4lw0.el4mlV8DOCzMb.37").get_all_ads_ids(
        user.email)
    else:
        if user.ads_ids:
            list_from_string = user.ads_ids.replace("{", "").replace("}", "").split(",")
            ads_ids = list_from_string + ads_ids

    #remove duplication
    ads_ids = list(dict.fromkeys(ads_ids))
    user.ads_ids = ads_ids
    db.session.add(user)
    db.session.commit()

    return "save_ads_ids"

@ads.route('/test')
def test():
    BazosHttp(
        "_ga=GA1.2.1097115696.1591092093; _gid=GA1.2.578207826.1591092093; bid=35797869; bkod=273WXWMGFP; testcookie=ano; __gfp_64b=k78R.IcLOGgD2nSd5M4F4fgtq4lw0.el4mlV8DOCzMb.37").get_ad_data("112419620")
    return "ddd"
