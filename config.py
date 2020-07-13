import os


class Config:
    SECRET_KEY = "U8mdsl0nwegd6belc"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:101478@localhost/bazos_bot'
