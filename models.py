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
        db.create_all()
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)

    def get_id(self):
        return self.id




# class Advertisement(db.Model):
#    __tablename__ = "ads"
#
#    id = db.Column(db.Integer, primary_key=True)
#    section = db.Column(db.String(60), nullable=False)
#    category = db.Column(db.String(60), nullable=False)
#    title = db.Column(db.String(60), nullable=False)
#    price = db.Column(db.String(20), nullable=False)
#    zip_code = db.Column(db.String(10), nullable=False)
#    category = db.Column(db.String(40), nullable=False)
