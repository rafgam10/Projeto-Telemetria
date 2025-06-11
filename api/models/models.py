from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Motoristas(db.Model):
    
    __tablename__ = "Motoristas"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    status = db.Column(db.String(20))
    
class Veiculos(db.Model):
    
    __tablename__ = "Veiculos"
    
    id_veiculo = db.Column(db.Integer, primary_key=True)
    pass