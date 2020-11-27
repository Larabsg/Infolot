from rede_social import app
from flask import render_template, redirect, url_for, request

#http://larabsg18.pythonanywhere.com

# Rotas para navegação
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

# Rotas para enviar/receber informações dos inputs

#Rota para o input de buscar usuário
@app.route('/buscar')
def buscar():
    busca = request.args['search']
    return f'busca:{busca}'

#Rota para inputs de login
@app.route('/info_login', methods=['POST'])
def info_login():
    email_login = request.form['email_login']
    senha_login = request.form['senha_login']
    return f'Email de login: {email_login}\nSenha de login: {senha_login}'

#Rota para inputs de cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome_cad = request.form['nome_cad']
    email_cad = request.form['email_cad']
    senha_cad = request.form['senha_cad']
    return f'{nome_cad} usa email {email_cad} e senha {senha_cad}'


