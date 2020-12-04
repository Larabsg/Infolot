from rede_social import app
import math
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
    #senha_login = request.form['senha_login']
    return render_template('feed.html', dados={'email': email_login})

#Rota para inputs de cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome_cad = request.form['nome_cad']
    email_cad = request.form['email_cad']
    senha_cad = request.form['senha_cad']
    return f'{nome_cad} usa email {email_cad} e senha {senha_cad}'

# Rota para funcionalidade geolocalização

#dicionario de teste para nao apresentar o erro ao procurar por 'lojas'
lojas = {'Maria': {'lat': -4.5921858, 'lon': -37.735278, 'area': 70.0, 'ocupacao': 0}}

@app.route('/checking', methods=['POST'])
def checking():
    lat = float(request.form['lat'])*math.pi/180
    lon = float(request.form['lon'])*math.pi/180
    loja = request.form['loja']

    l_cad = lojas[loja]

    l_lat = l_cad['lat']*math.pi/180
    l_lon = l_cad['lon']*math.pi/180
    l_a = l_cad['area']

    raio = math.sqrt(l_a/math.pi)

    deltaLng = l_lon - lon

    s = math.cos(math.pi/2 - l_lat)*math.cos(math.pi/2 - lat) + math.sin(math.pi/2 - l_lat)*math.sin(math.pi/2 - lat)*math.cos(deltaLng)
    arco = math.acos(s)

    distancia = arco*6378*1000

# Confere se a pessoa que fez checking está dentro ou fora da loja

    if distancia <= raio:
        l_cad['ocupacao'] += 1
        return render_template('feed.html', ocupacao={'conta': l_cad})
    else: 
        return f'Fora. Distância: {distancia} metros. Raio: {raio} metros'
    return f'Você está na loja {loja}'

