# admin/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.database_handler import motorista_dados, veiculo_dados, dados_relatorios
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
def pagina_admin():
    return render_template("HomeAdmin.html")

@admin_bp.route("/gestaoMotoristas", methods=["GET", "POST"])
def pagina_gestao_motoristas():
    motoristas = motorista_dados()
    return render_template("motoristasAdmin.html", motoristas=motoristas)

@admin_bp.route("/gestaoVeiculos", methods=["GET", "POST"])
def pagina_gestao_veiculos():
    veiculos = veiculo_dados()
    return render_template("veiculosAdmin.html", veiculos=veiculos)

@admin_bp.route("/inserirDados", methods=["GET", "POST"])
def pagina_inserir_dados():
    return render_template("importAdmin.html")

@admin_bp.route("/importar-excel", methods=["POST"])
def importar_Excel():
    if 'arquivo_excel' not in request.files:
        flash('Nenhum arquivo enviado', 'error')
        return redirect(url_for('admin.pagina_inserir_dados'))
    
    arquivo = request.files['arquivo_excel']
    if arquivo.filename == '':
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(url_for('admin.pagina_inserir_dados'))
    
    if not arquivo.filename.lower().endswith(('.xls', '.xlsx', '.xlsm')):
        flash('Formato de arquivo inválido. Envie um arquivo Excel.', 'error')
        return redirect(url_for('admin.pagina_inserir_dados'))
    
    try:
        caminho = os.path.join("uploads", arquivo.filename)
        arquivo.save(caminho)
        flash('Arquivo importado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao importar arquivo: {str(e)}', 'error')
    
    return redirect(url_for('admin.pagina_inserir_dados'))

@admin_bp.route("/relatorios", methods=["GET", "POST"])
def pagina_relatorios():
    motoristas = dados_relatorios()
    return render_template("relatorioAdmin.html", motoristas=motoristas)

@admin_bp.route("/logs", methods=["GET", "POST"])
def pagina_logs():
    return render_template("logsAdmin.html")
