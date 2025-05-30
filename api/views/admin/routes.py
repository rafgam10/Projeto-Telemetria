# admin/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.database_handler import conectar, motorista_dados, motorista_dados_unicos, veiculo_dados, veiculo_dados_unicos, dados_relatorios
import sqlite3
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
def pagina_admin():
    return render_template("HomeAdmin.html")

@admin_bp.route("/gestaoMotoristas", methods=["GET", "POST"])
def pagina_gestao_motoristas():
    motoristas = motorista_dados_unicos()
    return render_template("motoristasAdmin.html", motoristas=motoristas)

@admin_bp.route("/editar_motorista", methods=["POST"])
def editar_motorista():
    data = request.get_json()
    id_original = data.get('placa')
    motoristaDado =f"{data['id']} - {data['nome']}"

    # Exemplo com SQLite
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE DadosTelemetria
        SET motorista=?, marca_modelo=?, placa=?
        WHERE placa=?
    """, (
        motoristaDado, data['caminhao'], data['placa'],
        id_original
    ))

    conn.commit()
    conn.close()

    return jsonify({"success": True})


@admin_bp.route("/gestaoVeiculos", methods=["GET", "POST"])
def pagina_gestao_veiculos():
    veiculos = veiculo_dados_unicos()
    return render_template("veiculosAdmin.html", veiculos=veiculos)

@admin_bp.route("/editar_veiculos", methods=["POST"])
def editar_veiculos():
    data = request.get_json()
    frota = data['frota']
    modelo = data['modelo']
    marca = data['marca']
    placa = data['placa']
    status = data['status']
    placaId = data['placa']
    marca_modelo = f"{marca} / {modelo}"

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE DadosTelemetria SET marca_modelo=?, placa=?, frota=?
            WHERE placa=?
        """, (marca_modelo, placa, frota, placaId))
        conn.commit()
        conn.close()
        return jsonify({'mensagem': 'Veículo atualizado com sucesso'}), 200
    except Exception as e:
        print("Erro ao atualizar veículo:", e)
        return jsonify({'erro': 'Erro interno'}), 500


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




########################## teste ##############################

from flask import jsonify
from database.database_handler import user_dados

@admin_bp.route("/api/motorista/<placa>")
def api_dados_motorista(placa):
    dados = user_dados(placa.upper())

    if not dados:
        return jsonify({"erro": "Nenhum dado encontrado"}), 404

    consumos = []
    tempos = []
    labels = []

    for d in dados:
        try:
            media = float(d["media"])
            tempo_horas = float(d["total_hrs"]) / 60  # transforma minutos em horas
            if media > 0:
                consumos.append(round(media, 2))
                tempos.append(round(tempo_horas, 2))
                labels.append(d["data_chegada"])
        except:
            pass

    return jsonify({
        "motorista": dados[0]["motorista"],
        "placa": placa.upper(),
        "labels": labels,
        "consumos": consumos,
        "tempos": tempos
    })
