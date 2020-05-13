from flask import Blueprint, request, render_template, redirect
from ads.forms import AdForm

ads = Blueprint('ads', __name__)

@ads.route('/ads')
def advertisements():
    return render_template('advertisements.html')

@ads.route('/ads/add')
def add_advertisement():
    form = AdForm()
    return render_template('add_ad.html', form = form)



