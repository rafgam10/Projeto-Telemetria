# user/routes.py
from flask import Blueprint, render_template, session, redirect, url_for
from database.database_handler import user_dados

user_bp = Blueprint("user", __name__, url_prefix="/user")

@user_bp.route("/")
def pagina_user():
    placa = session.get("placa")
    if not placa:
        return redirect(url_for("exibir_login"))

    dados = user_dados(placa)

    for linha in dados:
        try:
            km = float(linha["km_rodado"])
            horas = float(linha["total_hrs"])
            diesel = float(linha["lt_diesel"])
            arla = float(linha["lt_arla"])
            linha["velocidade_media"] = round(km / horas, 2) if horas > 0 else 0
            linha["consumo_diesel"] = round((diesel / km) * 100, 2) if km > 0 else 0
            linha["consumo_arla"] = round((arla / km) * 100, 2) if km > 0 else 0
        except (ValueError, TypeError):
            linha["velocidade_media"] = 0
            linha["consumo_diesel"] = 0
            linha["consumo_arla"] = 0

    return render_template("HomeUser.html", dados=dados[-1] if dados else {})

@user_bp.route("/perfil")
def pagina_perfil():
    placa = session.get("placa")
    if not placa:
        return redirect(url_for("exibir_login"))

    dados = user_dados(placa)

    for linha in dados:
        try:
            km = float(linha["km_rodado"])
            horas = float(linha["total_hrs"])
            diesel = float(linha["lt_diesel"])
            arla = float(linha["lt_arla"])
            linha["velocidade_media"] = round(km / horas, 2) if horas > 0 else 0
            linha["consumo_diesel"] = round((diesel / km) * 100, 2) if km > 0 else 0
            linha["consumo_arla"] = round((arla / km) * 100, 2) if km > 0 else 0
        except (ValueError, TypeError):
            linha["velocidade_media"] = 0
            linha["consumo_diesel"] = 0
            linha["consumo_arla"] = 0
            
    return render_template('perfil.html', dados=dados)

@user_bp.route("/config", methods=["GET", "POST"])
def pagina_config():
    return render_template("config.html")

@user_bp.route("/suporte")
def pagina_suporte():
    return render_template("suporte.html")
