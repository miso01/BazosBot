from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

UPLOAD_FOLDER = '/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Musíte sa prihlásiť aby ste získali prístup k zadavanej stránke."
    login_manager.init_app(app)



    from auth.routes import auth
    from ads.routes import ads
    app.register_blueprint(auth)
    app.register_blueprint(ads)

    return app
