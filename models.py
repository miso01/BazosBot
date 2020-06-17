from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    cookie = db.Column(db.Text(), nullable=True)
    created_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)


class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    bazos_id = db.Column(db.String(30), nullable=True)
    section_text = db.Column(db.String(60), nullable=False)
    section_value = db.Column(db.String(60), nullable=False)
    category_text = db.Column(db.String(60), nullable=False)
    category_value = db.Column(db.String(60), nullable=False)
    title = db.Column(db.String(60), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    price_select = db.Column(db.Integer, nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    image_paths = db.Column(db.Text(), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    ad_password = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False)
    date_refresh = db.Column(db.DateTime(), nullable=False)##TODO RENAME
