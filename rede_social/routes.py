# from rede_social import create_app
import math
from flask import render_template, redirect, url_for, request, redirect, session, current_app as app
from rede_social import db, bcrypt
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
        if bcrypt.check_password_hash(alguem.senha, senha_login):
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

    # Verifica se email do usuário já é cadastrado no banco
    alguem = Usuario.query.filter_by(email = email_cad).first()

    if alguem is not None:

        return render_template('register.html', mensagem = 'Usuário já cadastrado')

    # Cadastra novo usuário ao banco
    else:
        novo = Usuario()
        novo.nome = nome_cad
        novo.email = email_cad
        # Criptografa senha
        senha_hash = bcrypt.generate_password_hash(senha_cad)#.decode('utf-8')

        novo.senha = senha_hash

        # Adiciona novo usuário ao banco e retorna à página de login
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
    area = request.form['areaLoja']
    #alerta = 'Cadastro realizado com sucesso!'

    loja = Loja.query.filter_by(cnpj = cnpj_cad_loja).first()

    if loja is not None:
        #session['mensagem'] = 'Usuário já cadastrado'
        return redirect('/cadastro_loja')

    else:
        novaLoja = Loja()
        novaLoja.nomeLoja = nome_cad_loja
        novaLoja.emailLoja = email_cad_loja

        # Crptografa senha da loja
        senha_hash_loja = bcrypt.generate_password_hash(senha_cad_loja)#.decode('utf-8')

        novaLoja.senhaLoja = senha_hash_loja
        novaLoja.limite = ocupacao_limite
        novaLoja.cnpj = cnpj_cad_loja
        novaLoja.latitude = latitude
        novaLoja.longitude = longitude
        novaLoja.area = area

        db.session.add(novaLoja)
        db.session.commit()
        return render_template('login.html')

# Gera uma página para as lojas cadastradas
@app.route('/feed/<int:id>')
def feed_loja(id):
    qualLoja = Loja.query.get(id)
    return render_template('feed.html',
                            nome = qualLoja.nomeLoja,
                            limite = qualLoja.limite
                            ) #faltando ocupacao, tirei p testar

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

    #check = request.form['check']
    recebeLongitude = request.form['lon']
    recebeLatitude = request.form['lat']
    latitude_calculada = float(recebeLatitude)*math.pi/180
    longitude_calculada = float(recebeLongitude)*math.pi/180
    nomeLoja = request.form['loja']

    # LatitudeDoBanco = Loja.query.filter_by(latitude = recebeLatitude).first()
    # LongitudeDoBanco = Loja.query.filter_by(longitude = recebeLongitude).first()
    #AreaDaLoja = Loja.query.get(area)
    loja = Loja.query.filter_by(nomeLoja = nomeLoja).first()
    LatitudeDoBanco = float(loja.latitude)
    LongitudeDoBanco = float(loja.longitude)
    #return loja.nomeLoja

    # l_cad = lojas[loja]

    l_lat = float(LatitudeDoBanco)*math.pi/180
    l_lon = float(LongitudeDoBanco)*math.pi/180
    l_a = float(loja.area)

    raio = math.sqrt(l_a/math.pi)

    deltaLng = l_lon - longitude_calculada

    s = math.cos(math.pi/2 - l_lat)*math.cos(math.pi/2 - latitude_calculada) + math.sin(math.pi/2 - l_lat)*math.sin(math.pi/2 - latitude_calculada)*math.cos(deltaLng)
    arco = math.acos(s)

    distancia = arco*6378*1000

# Confere se a pessoa que fez checking está dentro ou fora da loja
    ContaUm = loja.ocupacaoDaLoja
    if distancia <= raio:
        ContaUm = ContaUm + 1

        ''' Redirecionando errado quando clica no botao '''

        return render_template('feed.html', ContaUm = ContaUm)
    else:
        alert = 'Você não está nesta loja, tente fazer a contagem manual!'
        return render_template('feed.html', alerta = alert)
    #return f'Você está na loja {loja.nomeLoja}'

