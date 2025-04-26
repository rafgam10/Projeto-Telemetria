from flask import Flask
from flask_restful import Api, Resource
from models.motorista import MotoristaModel

app = Flask(__name__)
api = Api(app=app)


api.add_resource(MotoristaModel, "/")

if __name__ == "__main__":
    app.run(debug=True)
