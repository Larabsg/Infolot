from rede_social import app
from flask import render_template, redirect, url_for, request

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')
