from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)

# class Advertisement(db.Model):
#    __tablename__ = "advertisements"
#
#    id = db.Column(db.Integer, primary_key=True)
#    section = db.Column(db.String(60), nullable=False)
#    category = db.Column(db.String(60), nullable=False)
#    title = db.Column(db.String(60), nullable=False)
#    price = db.Column(db.String(20), nullable=False)
#    zip_code = db.Column(db.String(10), nullable=False)
#    category = db.Column(db.String(40), nullable=False)
