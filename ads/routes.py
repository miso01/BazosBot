from flask import Blueprint, request, render_template, redirect

ads = Blueprint('ads', __name__)

@ads.route('/ads')
def advertisements():
    return render_template('advertisements.html')



