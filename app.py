from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "U8mdsl0nwegd6belc"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
