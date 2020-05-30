import os

from flask import Blueprint, request, render_template, redirect, jsonify, url_for, flash
from datetime import datetime

from werkzeug.utils import secure_filename

from ads.forms import AdForm
from models import Advertisement, db
import utils
import flask_login
from flask_login import current_user
from __init__ import app

ads = Blueprint('ads', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@ads.route('/ads')
@flask_login.login_required
def advertisements():
    user_id = current_user.get_id()
    ads = Advertisement.query.filter_by(user_id=user_id).all()
    print("ads are toto " + str(ads) + " a user id je " + str(user_id))

    return render_template('advertisements.html', ads=ads)


@ads.route('/ads/add', methods=["POST", "GET"])
@flask_login.login_required
def add_advertisement():
    form = AdForm()
    if form.validate_on_submit():
        """ Custom validation for dynamic select field, wtforms doesnt support dynamic form validation"""
        if form.category.data:

            upload_files(form.image.data)

            category_text = utils.get_category_text_from_category_section_value(form.section.data, form.category.data)

            ad = Advertisement(
                user_id=current_user.get_id(),
                section_value=form.section.data,
                section_text=str(dict(form.section.choices).get(form.section.data)),
                category_value=form.category.data,
                category_text=category_text,
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
    return render_template('ad_detail.html', ad=ad)


@ads.route('/fetch_bazos_categories/<section>', methods=["POST", 'GET'])
@flask_login.login_required
def fetch_bazos_categories(section):
    # section = request.values.get("section", None)
    print("request values are + " + str(request.values))
    data = utils.fetch_bazos_categories(str(section))
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


def upload_files(image_field_data):
    if image_field_data:
        image_data = request.files.getlist("image")
        print("image data" + str(image_data))
        for img in image_data:
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
