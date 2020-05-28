from flask import Blueprint, request, render_template, redirect, url_for, flash
from models import User, db
from datetime import datetime
from __init__ import login_manager
from utils import flash_forms_errors
from auth.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_user

auth = Blueprint('auth', __name__)


@auth.route('/')
def home():
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    created_on=datetime.utcnow(), last_login=datetime.utcnow())
        if not User.query.filter_by(email=form.email.data).first():
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('ads.advertisements'))
        else:
            flash("Na tento e-mail už účet existuje.", category="auth")
            return render_template('register.html', form=form)
    else:
        flash_forms_errors(form)
        return render_template('register.html', form=form)


@auth.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            password = check_password_hash(user.password, form.password.data)
            if password:
                user.last_login = datetime.utcnow()
                db.session.commit()
                login_user(user)
                return redirect(url_for('ads.advertisements'))
            else:
                flash("Heslo nie je správne.", category="auth")
                return render_template('login.html', form=form)
        else:
            flash("Účet pre uvedený email neexistuje.", category="auth")
            return render_template('login.html', form=form)

    else:
        flash_forms_errors(form)
        return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

