from flask import Flask
from flask_cors import CORS
from .extensions import api
from .Views.Text import ns as text

app = Flask(__name__)
CORS(app)  # Permet toutes les origines d'accéder à ce serveur

# initialisation de restx
api.init_app(app)

# ajout du namespace defini dans views

api.add_namespace(text)