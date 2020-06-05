from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    def __init__(self, username, email, password, created_on, last_login):
        self.username = username
        self.email = email
        self.password = password
        self.created_on = created_on
        self.last_login = last_login

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)


class Advertisement(db.Model):
    __tablename__ = "ads"

    def __init__(self, user_id, section_text, section_value, category_text, category_value, title, text, price,
                 zip_code, image_paths, phone,
                 ad_password,
                 date_created, date_refreshed):
        self.user_id = user_id
        self.section_text = section_text
        self.section_value = section_value
        self.category_text = category_text
        self.category_value = category_value
        self.title = title
        self.text = text
        self.price = price
        self.zip_code = zip_code
        self.image_paths = image_paths
        self.phone = phone
        self.ad_password = ad_password
        self.date_created = date_created
        self.date_refresh = date_refreshed

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
    zip_code = db.Column(db.String(10), nullable=False)
    image_paths = db.Column(db.Text(), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    ad_password = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False)
    date_refresh = db.Column(db.DateTime(), nullable=False)
