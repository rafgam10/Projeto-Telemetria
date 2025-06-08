from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from database.admin_database.admin import (
    conectar, motorista_dados_unicos, veiculo_dados_unicos, dados_relatorios, dados_por_id_motorista
)
from datetime import datetime
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ================= Página Inicial =================
@admin_bp.route("/", methods=["GET"])
def pagina_admin():
    id_empresa = session.get('id_empresa')

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # Média de km por motorista da empresa
    cursor.execute("""
        SELECT COUNT(DISTINCT m.id) AS total_motoristas,
               SUM(m.distancia_total) AS total_km
        FROM Motoristas m
        JOIN Veiculos v ON m.veiculo_id = v.id
        WHERE v.empresa_id = %s
    """, (id_empresa,))
    resultado_km = cursor.fetchone()
    total_km = resultado_km["total_km"] or 0
    total_motoristas = resultado_km["total_motoristas"] or 1  # evita divisão por zero
    media_km_motorista = total_km / total_motoristas

    # Consumo de diesel do mês atual (baseado em data_final do veículo)
    mes_atual = datetime.now().strftime("%Y-%m")
    cursor.execute("""
        SELECT 
            SUM(v.distancia_viagem) AS km,
            SUM(v.litros_consumidos) AS diesel
        FROM Veiculos v
        WHERE v.empresa_id = %s AND DATE_FORMAT(v.data_final, '%%Y-%%m') = %s
    """, (id_empresa, mes_atual))
    resultado = cursor.fetchone()
    km_mes = resultado["km"] or 0
    diesel_mes = resultado["diesel"] or 0
    consumo_diesel_mes = km_mes / diesel_mes if diesel_mes else 0

    cursor.close()
    conn.close()

    return render_template("HomeAdmin.html",
        id_empresa=id_empresa,
        media_km_motorista=round(media_km_motorista, 2),
        consumo_diesel_mes=round(consumo_diesel_mes, 2)
    )

# ========== Gestão de Motoristas ==========
@admin_bp.route("/gestaoMotoristas", methods=["GET", "POST"])
def pagina_gestao_motoristas():
    idEmpresa = session.get('id_empresa')
    motoristas = motorista_dados_unicos(idEmpresa)
    return render_template("motoristasAdmin.html", motoristas=motoristas)

# ========== Gestão de Veículos ==========
@admin_bp.route("/gestaoVeiculos", methods=["GET", "POST"])
def pagina_gestao_veiculos():
    idEmpresa = session.get("id_empresa")
    veiculos = veiculo_dados_unicos(idEmpresa)
    return render_template("veiculosAdmin.html", veiculos=veiculos)

# ========== Importar Dados ==========
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

    if not arquivo.filename.lower().endswith(('.xls', '.xlsx', '.xlsm', '.csv')):
        flash('Formato de arquivo inválido. Envie um arquivo Excel.', 'error')
        return redirect(url_for('admin.pagina_inserir_dados'))

    try:
        caminho = os.path.join("uploads", arquivo.filename)
        arquivo.save(caminho)
        flash('Arquivo importado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao importar arquivo: {str(e)}', 'error')

    return redirect(url_for('admin.pagina_inserir_dados'))

# ========== Relatórios ==========
@admin_bp.route("/relatorios", methods=["GET", "POST"])
def pagina_relatorios():
    motoristas = dados_relatorios()
    return render_template("relatorioAdmin.html", motoristas=motoristas)

# ========== Metas ==========
@admin_bp.route("/metas", methods=["GET", "POST"])
def pagina_metas():
    return render_template("metasAdmin.html")

# ========== API para dados por motorista ==========
@admin_bp.route("/api/motorista-id/<int:id_motorista>")
def api_dados_por_id_motorista(id_motorista):
    dados = dados_por_id_motorista(id_motorista)

    if not dados:
        return jsonify({"erro": "Nenhum dado encontrado"}), 404

    consumos = []
    tempos = []
    labels = []

    for d in dados:
        try:
            media = float(d["media_km_l"])
            tempo_horas = float(d["total_hrs"]) / 60
            data = d["data_final"]

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
