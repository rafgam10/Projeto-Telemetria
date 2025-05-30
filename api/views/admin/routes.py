# admin/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database.database_handler import motorista_dados, motorista_dados_unicos, veiculo_dados, veiculo_dados_unicos, dados_relatorios
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
def pagina_admin():
    return render_template("HomeAdmin.html")

@admin_bp.route("/gestaoMotoristas", methods=["GET", "POST"])
def pagina_gestao_motoristas():
    motoristas = motorista_dados_unicos()
    return render_template("motoristasAdmin.html", motoristas=motoristas)

@admin_bp.route("/gestaoVeiculos", methods=["GET", "POST"])
def pagina_gestao_veiculos():
    veiculos = veiculo_dados_unicos()
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




########################## relatorio ##############################

from flask import jsonify
from database.database_handler import dados_por_id_motorista

@admin_bp.route("/api/motorista-id/<id_motorista>")
def api_dados_por_id_motorista(id_motorista):
    id_motorista = id_motorista.upper().strip()
    dados = dados_por_id_motorista(id_motorista)

    if not dados:
        return jsonify({"erro": "Nenhum dado encontrado"}), 404

    consumos = []
    tempos = []
    labels = []

    for d in dados:
        try:
            media = float(d["media"])
            tempo_horas = float(d["total_hrs"]) / 60
            data = d.get("data_chegada") or d.get("data")

            if media > 0:
                consumos.append(round(media, 2))
                tempos.append(round(tempo_horas, 2))
                labels.append(data)
        except:
            continue

    return jsonify({
        "motorista": dados[0]["motorista"],
        "labels": labels,
        "consumos": consumos,
        "tempos": tempos
    })
