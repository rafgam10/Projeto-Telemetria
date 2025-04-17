from flask_restful import Resource
from flask import jsonify

motoristaModel = {
    "Nome": "João da Silva",
    "Data": "01/04/2025",
    "Km/h": 110,
    "Km/l": 8.5,
    "Km Rodados": 125
}

class MotoristaModel(Resource):
    
    def get(self):
        return jsonify(motoristaModel) 
