from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MotoristaModel(db.Model):
    __tablename__ = "motoristas"

    id = db.Column(db.Integer, primary_key=True)
    motorista = db.Column(db.String)
    placa = db.Column(db.String)
    frota = db.Column(db.String)
    marca = db.Column(db.String)

    data = db.Column(db.String)
    datasSaida = db.Column(db.String)
    dataChegada = db.Column(db.String)
    qtdDias = db.Column(db.Integer)
    totalHrs = db.Column(db.Integer)

    KmSaida = db.Column(db.Integer)
    KmChegada = db.Column(db.Integer)
    KmRodado = db.Column(db.Integer)

    LtArla = db.Column(db.Float)
    LtDiesel = db.Column(db.Float)
    LtPorDia = db.Column(db.Float)

    def __repr__(self):
        return f"<Motorista {self.motorista}>"
