# api/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.database_handler import conectar, motorista_dados, motorista_dados_unicos, veiculo_dados, veiculo_dados_unicos, dados_relatorios
from database.admin_database.admin import adicionar_motorista_banco, motorista_dados_unicos, veiculo_dados_unicos
import sqlite3
from datetime import datetime
import os

api_bp = Blueprint("api", __name__, url_prefix="/api")



