from main import app
from flask import render_template, redirect,request,flash,session,url_for
from controller.models import *

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return "About"