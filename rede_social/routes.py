from rede_social import app
from flask import render_template, redirect, url_for, request

#http://larabsg18.pythonanywhere.com

@app.route('/')
def homepage():
    usuario_logado = False
    return render_template('index.html', logado = usuario_logado)

@app.route('/sobre')
def aboutpage():
    return render_template('about.html')

@app.route('/contato')
def contactpage():
    return render_template('contact.html')

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/cadastro')
def registerpage():
    return render_template('register.html')

@app.route('/feed')
def feedpage():
    return render_template('feed.html')

@app.route('/redefinir_senha')
def redefinirpage():
    return render_template('redefinir.html')

@app.route('/contador_manual')
def contador_manual():
    return render_template('contador_manual.html')

@app.route('/buscar')
def buscar():
    busca = request.args['search']
    return f'busca:{busca}'

@app.route('/info_login')
def info_login():
    email_login = request.form['email_login']
    senha_login = request.form['senha_login']
    return email_login, senha_login


