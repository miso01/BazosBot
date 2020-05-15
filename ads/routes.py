from flask import Blueprint, request, render_template, redirect, jsonify, url_for
from werkzeug.utils import secure_filename
from datetime import datetime

from ads.forms import AdForm
from models import Advertisement, db
import utils

ads = Blueprint('ads', __name__)


@ads.route('/ads')
def advertisements():
    ads = Advertisement.query.all()
    print("ads are toto " + str(ads))

    return render_template('advertisements.html', ads=ads)


@ads.route('/ads/add', methods=["POST", "GET"])
def add_advertisement():
    form = AdForm()
    if request.method == "POST":
        # filename = secure_filename(form.image.data.filename)
        # form.file.data.save('uploads/' + filename)

        print("args je " + str(request.args))
        print("values je " + str(request.form.values()))

        print("choices " + str(form.section.choices))
        print("choices " + str(form.category.choices))
        print("text " + str(dict(form.section.choices).get(form.section.data)) + " value   " + form.section.data)
        print("text " + str(dict(request.values).get(form.category.data)) + " value   " + form.category.data)

        ad = Advertisement(
            section_value=form.section.data,
            section_text="ddd",
            category_value=form.category.data,
            category_text="ddd",
            title=form.title.data,
            text=form.text.data,
            price=form.price.data,  # TODO validate
            zip_code=form.zip_code.data,
            phone=form.phone.data,
            ad_password=form.ad_password.data,
            date_created=datetime.utcnow(),
            date_refreshed=datetime.utcnow())
        db.session.add(ad)
        db.session.commit()
        return redirect(url_for('ads.advertisements'))
    else:
        return render_template('add_ad.html', form=form)


@ads.route('/ads/edit')
def edit_advertisement():
    form = AdForm()
    if request.method == "POST":
        pass


@ads.route('/fetch_bazos_categories/', methods=["POST"])
def fetch_bazos_categories():
    section = request.values.get("section", None)
    print("request values are + " + str(request.values))
    data = utils.fetch_bazos_categories(section)
    print("section is " + section + " a data su " + str(data))
    return jsonify(data)
