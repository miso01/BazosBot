from flask import Blueprint, request, render_template, redirect, jsonify, url_for
from datetime import datetime
from ads.forms import AdForm
from models import Advertisement, db
import utils
import flask_login
from flask_login import current_user

ads = Blueprint('ads', __name__)


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
    if request.method == "POST":
        # filename = secure_filename(form.image.data.filename)
        # form.file.data.save('uploads/' + filename)

        print("choices " + str(form.section.choices))
        print("choices " + str(form.category.choices))
        print("text " + str(dict(form.section.choices).get(form.section.data)) + " value   " + form.section.data)
        print("text " + str(dict(request.values).get(form.category.data)) + " value   " + form.category.data)

        ad = Advertisement(
            user_id=current_user.get_id(),
            section_value=form.section.data,
            section_text="Section Text",
            category_value=form.category.data,
            category_text="Category Text",
            title=form.title.data,
            text=form.text.data,
            price=form.price.dta,  # TODO validate
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


@flask_login.login_required
@ads.route('/ads/edit/<int:ad_id>', methods=["POST", "GET"])
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


@flask_login.login_required
@ads.route('/fetch_bazos_categories/', methods=["POST"])
def fetch_bazos_categories():
    section = request.values.get("section", None)
    print("request values are + " + str(request.values))
    data = utils.fetch_bazos_categories(section)
    print("section is " + section + " a data su " + str(data))
    return jsonify(data)


@flask_login.login_required
@ads.route('/ads/delete/<int:ad_id>')
def delete_advertisement(ad_id):
    ad = Advertisement.query.get_or_404(ad_id)
    db.session.delete(ad)
    db.session.commit()
    return redirect(url_for('ads.advertisements'))
