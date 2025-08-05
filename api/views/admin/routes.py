from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from database.admin_database.admin import (
    conectar, motorista_dados_unicos, veiculo_dados_unicos, motoristas_unicos_por_empresa, dados_relatorios, dados_por_id_motorista
)
from database.importações_database.importacoes import (
    listar_importacoes_db
)
from excel_importer.excel_json import importar_dados_excel_mysql
from utils.util import *
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

    melhores_motoristas = top_motoristas(id_empresa)

    return render_template("HomeAdmin.html",
        id_empresa=id_empresa,
        media_km_motorista=round(media_km_motorista, 2),
        consumo_diesel_mes=round(consumo_diesel_mes, 2),
        melhores_motoristas=melhores_motoristas
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

        empresa_id = session.get('id_empresa') or 1  # Substituir por valor real em produção
        registros = importar_dados_excel_mysql(caminho, empresa_id)

        # Remover o arquivo após a importação
        os.remove(caminho)

        flash(f'{registros} registros importados com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao importar arquivo: {str(e)}', 'error')

    return redirect(url_for('admin.pagina_inserir_dados'))

# ========== Relatórios ==========
@admin_bp.route("/relatorios", methods=["GET", "POST"])
def pagina_relatorios():
    id_empresa = session.get("id_empresa")
    motoristas = motoristas_unicos_por_empresa(id_empresa)
    return render_template("relatorioAdmin.html", motoristas=motoristas)


# ========== listaimportação ==========
@admin_bp.route("/listaImportacoes", methods=["GET", "POST"])
def lista_importacoes():
    id_empresa = session.get("id_empresa")
    importacoes = listar_importacoes_db(id_empresa)
    return render_template("listaImportacoes.html", importacoes=importacoes)


# ========== Metas ==========
@admin_bp.route("/metas", methods=["GET", "POST"])
def pagina_metas():
    id_empresa = session.get("id_empresa")
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # Dentro do if request.method == "POST":
    if request.method == "POST":
        print("🟡 POST recebido em /admin/metas")
        for key, value in request.form.items():
            if key.startswith("meta_"):
                try:
                    marca_modelo = key.replace("meta_", "")
                    partes = marca_modelo.split("_")
                    marca = partes[0]
                    modelo = "_".join(partes[1:])
                    nova_meta = float(value)

                    marca_sql = marca.replace("_", " ")
                    modelo_sql = modelo.replace("_", " ")

                    print(f"🛠️ Atualizando meta: marca='{marca_sql}', modelo='{modelo_sql}', nova_meta={nova_meta}")

                    cursor.execute("""
                        UPDATE MetasConsumo
                        SET meta_km_por_litro = %s
                        WHERE empresa_id = %s AND marca = %s AND modelo = %s
                    """, (nova_meta, id_empresa, marca_sql, modelo_sql))

                    # ⬇️ Recalcula notas dos motoristas desse modelo
                    calcular_notas_motoristas(conn, id_empresa)

                except Exception as e:
                    print(f"❌ Erro ao atualizar meta para {key}: {e}")
                    flash("Erro ao atualizar metas!", "danger")

        conn.commit()
        flash("Metas atualizadas com sucesso!", "success")
        return redirect(url_for("admin.pagina_metas"))



    # Busca inicial para exibir metas
    cursor.execute("""
        SELECT marca, modelo, meta_km_por_litro
        FROM MetasConsumo
        WHERE empresa_id = %s
        ORDER BY marca, modelo
    """, (id_empresa,))
    veiculos = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("metasAdmin.html", veiculos=veiculos)


# ========== API para dados por motorista ==========
@admin_bp.route("/api/motorista-id/<int:id_motorista>")
def api_dados_por_id_motorista(id_motorista):
    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    # 1. Buscar o nome do motorista pelo ID
    cursor.execute("SELECT nome FROM Motoristas WHERE id = %s", (id_motorista,))
    motorista = cursor.fetchone()

    if not motorista:
        conn.close()
        return jsonify({"erro": "Motorista não encontrado"}), 404

    nome_motorista = motorista["nome"]

    # 2. Buscar todos os registros com o mesmo nome
    cursor.execute("""
        SELECT 
            M.data_final,
            M.consumo_medio,
            M.distancia_total,
            V.placa
        FROM Motoristas M
        JOIN Veiculos V ON M.veiculo_id = V.id
        WHERE M.nome = %s
        ORDER BY M.data_final ASC
    """, (nome_motorista,))
    
    registros = cursor.fetchall()
    cursor.close()
    conn.close()

    if not registros:
        return jsonify({"erro": "Nenhum dado encontrado"}), 404

    labels = []
    consumos = []
    distancias = []
    placa = registros[-1]["placa"]  # Última placa usada (mais recente)

    for r in registros:
        try:
            labels.append(r["data_final"].strftime("%Y-%m-%d"))
            consumos.append(float(r["consumo_medio"]))
            distancias.append(float(r["distancia_total"]))
        except Exception:
            continue

    if not consumos:
        return jsonify({"erro": "Registros inválidos"}), 400

    return jsonify({
        "motorista": nome_motorista,
        "placa": placa,
        "labels": labels,
        "consumos": consumos,
        "distancias": distancias,
        "media_consumo": round(sum(consumos) / len(consumos), 2),
        "melhor_consumo": max(consumos),
        "pior_consumo": min(consumos)
    })
