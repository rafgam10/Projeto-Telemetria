# user/routes.py
from flask import Blueprint, render_template, session, redirect, url_for
from database.database_handler import user_dados 
from database.user_database.user import *

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/")
def pagina_user():
    placa = session.get("placa")
    if not placa:
        return redirect(url_for("exibir_login"))

    dados = user_dados(placa)
    if not dados:
        return render_template("HomeUser.html", dados={})

    return render_template("HomeUser.html", dados=dados)

@user_bp.route("/perfil")
def pagina_perfil():
    placa = session.get("placa")
    if not placa:
        return redirect(url_for("exibir_login"))

    dados = user_dados(placa)
    historico = historico_motorista(placa)
    perfil = perfil_user(placa)

    if not dados or not perfil:
        return render_template("perfil.html", dados=[], historico=[])

    return render_template("perfil.html", dados=dados, historico=historico)

@user_bp.route("/config", methods=["GET", "POST"])
def pagina_config():
    return render_template("config.html")

@user_bp.route("/suporte")
def pagina_suporte():
    return render_template("suporte.html")
