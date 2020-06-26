from flask_login import UserMixin
from __init__ import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    cookie = db.Column(db.Text(), nullable=True)
    ad_password = db.Column(db.String(60), nullable=True)
    created_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)
    ads = db.relationship("Advertisement", backref="user")


class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ad_id = db.Column(db.String(9), nullable=False, unique=True)
    interval = db.Column(db.Integer, nullable=False)
    refresh_date = db.Column(db.DateTime, nullable=False)


# class Advertisement:
#
#     def __init__(self, category, nadpis, popis, cena, cenavyber, lokalita, jmeno, telefoni, maili, heslobazar,
#                  rterte="gdfgdfga", Submit="Odoslať"):
#         self.category = category
#         self.nadpis = nadpis
#         self.popis = popis
#         self.cena = cena
#         self.cenavyber = cenavyber
#         self.lokalita = lokalita
#         self.jmeno = jmeno
#         self.telefoni = telefoni
#         self.maili = maili
#         self.heslobazar = heslobazar
#         self.rterte = rterte
#         self.Submit = Submit
