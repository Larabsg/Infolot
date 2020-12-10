# from rede_social import create_app
import math
from flask import render_template, redirect, url_for, request, redirect, session, current_app as app
from rede_social import db
from rede_social.entidades import Usuario, Loja

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

@app.route('/cadastro_loja')
def register_store():
    return render_template('register_store.html')



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
    email_login = request.form['email_user']
    senha_login = request.form['senha_user']

    alguem = Usuario.query.filter_by(email = email_login).first()

    if alguem is not None:
        if senha_login == alguem.senha:
            return render_template('feed.html')
        else:
            return render_template('login.html', mensagemSenha = 'Senha inválida')
    else:
        return render_template('login.html', mensagemUserInex = 'Usuário inexistente')

#Rota para inputs de cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome_cad = request.form['nome_user']
    email_cad = request.form['email_user']
    senha_cad = request.form['senha_user']

#Verifica se email do usuário já é cadastrado no banco
    alguem = Usuario.query.filter_by(email = email_cad).first()

    if alguem is not None:
        #mensagem = 'Usuário já cadastrado'
        return render_template('register.html', mensagem = 'Usuário já cadastrado')

#Cadastra novo usuário ao banco
    else:
        novo = Usuario()
        novo.nome = nome_cad
        novo.email = email_cad
        novo.senha = senha_cad

#Adiciona novo usuário ao banco e retorna à página de login
        db.session.add(novo)
        db.session.commit()
        return render_template('login.html')

@app.route('/cadastrar/loja', methods=['POST'])
def cadastrar_loja():
    nome_cad_loja = request.form['nome_loja']
    cnpj_cad_loja = request.form['cnpj_loja']
    email_cad_loja = request.form['email_loja']
    senha_cad_loja = request.form['senha_loja']
    ocupacao_limite = request.form['ocupacao_limite']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    #alerta = 'Cadastro realizado com sucesso!'
    
    loja = Loja.query.filter_by(cnpj = cnpj_cad_loja).first()

    if loja is not None:
        #session['mensagem'] = 'Usuário já cadastrado'
        return redirect('/cadastro_loja')

    else:
        novaLoja = Loja()
        novaLoja.nomeLoja = nome_cad_loja
        novaLoja.emailLoja = email_cad_loja
        novaLoja.senhaLoja = senha_cad_loja
        novaLoja.limite = ocupacao_limite
        novaLoja.cnpj = cnpj_cad_loja
        novaLoja.latitude = latitude
        novaLoja.longitude = longitude

        db.session.add(novaLoja)
        db.session.commit()
        return render_template('login.html')

# Remove alguém do banco
@app.route('/remove/<int:id>')
def remove(id):
    quem = Usuario.query.get(id)
    db.session.delete(quem)
    db.session.commit()
    return f'Removi o usuário {quem.nome}'

# Remove loja do banco
@app.route('/remove/loja/<int:id>')
def removeLoja(id):
    quemLoja = Loja.query.get(id)
    db.session.delete(quemLoja)
    db.session.commit()
    return f'Removi a loja {quemLoja.nomeLoja}'

# Rota para funcionalidade geolocalização

#dicionario de teste para nao apresentar o erro ao procurar por 'lojas'
#lojas = {'Maria': {'lat': -4.5921858, 'lon': -37.735278, 'area': 1000.0, 'ocupacao': 0}}

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
        return render_template('feed.html', dados = l_cad['ocupacao'])
    else: 
        return f'Fora. Distância: {distancia} metros. Raio: {raio} metros'
    return f'Você está na loja {loja}'

