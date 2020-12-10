from rede_social import db
from datetime import datetime
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(1000), nullable=False)

class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomeLoja = db.Column(db.String(100), unique=True, nullable=False)
    emailLoja = db.Column(db.String(100), unique=True, nullable=False)
    limite = db.Column(db.Integer, nullable=False)
    cnpj = db.Column(db.String(100), unique=True, nullable=False)
    latitude = db.Column(db.String(100), unique=True, nullable=False)
    longitude = db.Column(db.String(100), unique=True, nullable=False)
    senhaLoja = db.Column(db.String(100), nullable=False)
