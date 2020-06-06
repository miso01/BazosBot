import os
from flask import Blueprint, request, render_template, redirect, jsonify, url_for, flash
from datetime import datetime
from werkzeug.utils import secure_filename
from ads.forms import AdForm
from bazos_http import BazosHttp
from models import Advertisement, User, db
import utils
import flask_login
from flask_login import current_user
from __init__ import app

ads = Blueprint('ads', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@ads.route('/ed')
def ed():
    bh = BazosHttp()
    #bh.post_advertisement(Advertisement, User, db)
    #bh.delete_advertisement(Advertisement)
    return "Pridany unzerat"


@ads.route('/ads')
@flask_login.login_required
def advertisements():
    user_id = current_user.get_id()
    ads = Advertisement.query.filter_by(user_id=user_id).all()
    for ad in ads:
        ad.image_paths = ad.image_paths.replace("{", "").replace("}", "").split(",")

    return render_template('advertisements.html', ads=ads)


@ads.route('/ads/add', methods=["POST", "GET"])
@flask_login.login_required
def add_advertisement():
    form = AdForm()
    form.price_select
    if form.validate_on_submit():
        """ Custom validation for dynamic select field, wtforms doesnt support dynamic form validation"""
        if form.category.data:

            category_text = utils.get_category_text_from_category_section_value(form.section.data, form.category.data)

            ad = Advertisement(
                user_id=current_user.get_id(),
                section_value=form.section.data,
                section_text=str(dict(form.section.choices).get(form.section.data)),
                category_value=form.category.data,
                category_text=category_text,
                title=form.title.data,
                text=form.text.data,
                image_paths=[],
                price=form.price.data,  # TODO validate
                price_select=form.price_select.data,
                zip_code=form.zip_code.data,
                phone=form.phone.data,
                ad_password=form.ad_password.data,
                date_created=datetime.utcnow(),
                date_refreshed=datetime.utcnow())
            db.session.add(ad)
            db.session.flush()

            print("ad id after flush je " + str(ad.id))
            image_paths = upload_files(form.image.data, ad.id)

            ad.image_paths = image_paths

            db.session.commit()
            return redirect(url_for('ads.advertisements'))
        else:
            flash("K pridaniu inzerátu je potrebné zvoliť kategóriu.")
            return render_template('add_ad.html', form=form)
    else:
        utils.flash_forms_errors(form)
        return render_template('add_ad.html', form=form)


@ads.route('/ads/edit/<int:ad_id>', methods=["POST", "GET"])
@flask_login.login_required
def edit_advertisement(ad_id):
    ad = Advertisement.query.get_or_404(ad_id)

    form = AdForm()
    if request.method == "POST":
        ad.section_value = form.section.data
        ad.section_text = "Section Text"
        ad.category_value = form.category.data
        ad.category_text = "Category Text"
        ad.title = form.title.data
        ad.text = form.text.data
        ad.price = form.price.data  # TODO validate
        ad.zip_code = form.zip_code.data
        ad.phone = form.phone.data
        ad.ad_password = form.ad_password.data
        ad.date_refreshed = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('ads.advertisements'))
    else:
        return render_template('edit_add.html', ad=ad, form=AdForm())
    pass


@ads.route('/ads/<int:ad_id>')
@flask_login.login_required
def ad_detail(ad_id):
    ad = Advertisement.query.filter_by(id=ad_id).first()
    ad.image_paths = ad.image_paths.replace("{", "").replace("}", "").split(",")

    return render_template('ad_detail.html', ad=ad)


@ads.route('/fetch_bazos_categories/<section>', methods=["POST", 'GET'])
@flask_login.login_required
def fetch_bazos_categories(section):
    print("request values are + " + str(request.values))
    data = BazosHttp().fetch_bazos_categories(str(section))
    categories = []
    for category in data:
        value = category[0].replace("/", "")
        ctg = {"value": value, "category_text": category[1]}
        categories.append(ctg)

    return jsonify({"categories": categories})


@ads.route('/ads/delete/<int:ad_id>')
@flask_login.login_required
def delete_advertisement(ad_id):
    ad = Advertisement.query.get_or_404(ad_id)
    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('ads.advertisements'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_files(image_field_data, ad_id):
    image_paths = []
    if image_field_data:
        image_data = request.files.getlist("image")
        print("image data" + str(image_data))
        if len(image_data) > 0:
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + str(ad_id)))
            for img in image_data:
                filename = secure_filename(img.filename)
                img.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + str(ad_id), filename))
                image_paths.append("uploads/" + str(ad_id) + "/" + str(filename))
    return image_paths


def log_request(r):
    print("raw " + str(r.raw))
    print("content " + str(r.content))
    print("text " + str(r.text))
    print("links " + str(r.links))
    print("next " + str(r.next))
    print("ok " + str(r.ok))
    print("headers " + str(r.headers))
    print("request " + str(r.request))
    print("status code " + str(r.status_code))
    print("reason " + str(r.reason))
    print("url " + str(r.url))
    print("cookies " + str(r.cookies))
    print("encoding  " + str(r.encoding))
    print("hisotry " + str(r.history))
    print("elapsed " + str(r.elapsed))
