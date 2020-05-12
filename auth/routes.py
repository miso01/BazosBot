from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import User, db
from datetime import datetime
from __init__ import login_manager
from utils import flash_forms_errors

from auth.forms import RegisterForm, LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data,
                    created_on=datetime.utcnow(), last_login=datetime.utcnow())
        if not User.query.filter_by(email=form.email.data).first():
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('ads.advertisements'))
        else:
            flash("Na tento e-mail už účet existuje.", category="auth")
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@auth.route('/login',methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user:
            user.last_login = datetime.utcnow()
            return redirect(url_for('ads.advertisements'))
        else:
            flash("Najprv sa musíte zargistrovať.", category="auth")
            return render_template('login.html', form=form)

    else:
        flash_forms_errors(form)
        return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
