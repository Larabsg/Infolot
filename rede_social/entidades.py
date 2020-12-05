from rede_social import db
from datetime import datetime
class Usuario(db.Models):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unic=True, nullabel=False)
    senha = db.Column(db.String(1000), nullabel=False)