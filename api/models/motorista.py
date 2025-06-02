from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Motorista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    status = db.Column(db.String(20))