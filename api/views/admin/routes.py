# admin/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database.admin_database.admin import conectar, adicionar_motorista_banco, motorista_dados_unicos, veiculo_dados_unicos, motorista_dados_unicos_editar, dados_relatorios
from database.admin_database.admin import adicionar_motorista_banco, adicionar_veiculo_banco
import sqlite3
from datetime import datetime
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/", methods=["GET"])
def pagina_admin():
    conn = sqlite3.connect("api/database/telemetria.db")
    cursor = conn.cursor()

    # Total de viagens
    cursor.execute("SELECT COUNT(*) FROM DadosTelemetria")
    total_viagens = cursor.fetchone()[0]

    # Média de km por motorista
    cursor.execute("SELECT id_motorista, SUM(km_rodado) FROM DadosTelemetria GROUP BY id_motorista")
    km_por_motorista = cursor.fetchall()
    media_km_motorista = sum([linha[1] for linha in km_por_motorista]) / len(km_por_motorista) if km_por_motorista else 0

    # Consumo mensal de diesel e arla (considerando mês atual)
    mes_atual = datetime.now().strftime("%Y-%m")
    cursor.execute("""
        SELECT SUM(km_rodado), SUM(consumo_diesel), SUM(consumo_arla)
        FROM DadosTelemetria
        WHERE substr(data_registro, 1, 7) = ?
    """, (mes_atual,))
    resultado = cursor.fetchone()
    km_mes, diesel_mes, arla_mes = resultado if resultado else (0, 0, 0)

    consumo_diesel_mes = (km_mes / diesel_mes) if diesel_mes else 0
    consumo_arla_mes = (km_mes / arla_mes) if arla_mes else 0

    cursor.execute("SELECT id_empresa FROM DadosTelemetria")
    id_empresa = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template("HomeAdmin.html",
        id_empresa = id_empresa,
        total_viagens=total_viagens,
        media_km_motorista=round(media_km_motorista, 2),
        consumo_diesel_mes=round(consumo_diesel_mes, 2),
        consumo_arla_mes=round(consumo_arla_mes, 2)
    )

#### Gerenciamento de Motoristas #################
@admin_bp.route("/gestaoMotoristas", methods=["GET", "POST"])
def pagina_gestao_motoristas():
    idEmpresa = session.get('id_empresa')
    motoristas = motorista_dados_unicos(idEmpresa)
    return render_template("motoristasAdmin.html", motoristas=motoristas)

@admin_bp.route("/editar_motorista", methods=["POST"])
def editar_motorista():
    data = request.get_json()
    
    id_motorista = data.get("id_motorista")
    nome = data.get("nome")
    status = data.get("status")
    marca_modelo = data.get("caminhao")  # Exemplo: "VOLVO / FH 460"
    placa = data.get("placa")

    # Divide marca e modelo
    try:
        marca, modelo = [x.strip() for x in marca_modelo.split("/", 1)]
    except ValueError:
        print("1")
        return jsonify({"success": False, "message": "Caminhão inválido. Use 'Marca / Modelo'."}), 400

    dados = motorista_dados_unicos_editar(id_motorista)
    if not dados:
        print("2")
        return jsonify({"success": False, "message": "Motorista não encontrado"}), 404

    id_veiculo = dados["id_veiculo"]
    
    conn = conectar()
    cursor = conn.cursor()

    # Atualiza Motorista
    cursor.execute("""
        UPDATE Motoristas
        SET nome = ?, status = ?
        WHERE id_motorista = ?
    """, (nome, status, id_motorista))

    # Atualiza Veículo
    cursor.execute("""
        UPDATE Veiculos
        SET marca = ?, modelo = ?, placa = ?
        WHERE id_veiculo = ?
    """, (marca, modelo, placa, id_veiculo))

    conn.commit()
    conn.close()

    return jsonify({"success": True}), 200

@admin_bp.route('/deletar_motorista/<int:id>', methods=['DELETE'])
def deletar_motorista(id):
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Verifica se o motorista existe
        cursor.execute("SELECT * FROM Motoristas WHERE id_motorista = ?", (id,))
        motorista = cursor.fetchone()

        if not motorista:
            return jsonify({'erro': 'Motorista não encontrado.'}), 404

        # Deleta motorista
        cursor.execute("DELETE FROM Motoristas WHERE id_motorista = ?", (id,))
        conn.commit()
        return jsonify({'mensagem': 'Motorista deletado com sucesso!'}), 200

    except sqlite3.Error as e:
        return jsonify({'erro': f'Erro no banco de dados: {str(e)}'}), 500

    finally:
        conn.close()
        
################################################################


########## Gereciamento de Veiculos ##################################
@admin_bp.route("/gestaoVeiculos", methods=["GET", "POST"])
def pagina_gestao_veiculos():
    idEmpresa = session.get("id_empresa")
    veiculos = veiculo_dados_unicos(idEmpresa)
    return render_template("veiculosAdmin.html", veiculos=veiculos)

@admin_bp.route("/editar_veiculos", methods=["POST"])
def editar_veiculos():
    data = request.get_json()
    
    id_veiculo = data.get("id_veiculo")  # <-- melhor usar ID fixo
    frota = data.get("frota")
    modelo = data.get("modelo")
    marca = data.get("marca")
    placa = data.get("placa")
    status = data.get("status")

    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE Veiculos
            SET marca = ?, modelo = ?, placa = ?, frota = ?, status = ?
            WHERE id_veiculo = ?
        """, (marca, modelo, placa, frota, status, id_veiculo))

        conn.commit()
        conn.close()

        return jsonify({'mensagem': 'Veículo atualizado com sucesso'}), 200
    except Exception as e:
        print("Erro ao atualizar veículo:", e)
        return jsonify({'erro': 'Erro interno'}), 500


@admin_bp.route('/deletar_veiculo/<int:id>', methods=['POST'])
def deletar_veiculo(id):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Veiculos WHERE id_veiculo = ?", (id,))
        veiculo = cursor.fetchone()

        if not veiculo:
            return jsonify({'erro': 'Veiculo não encontrado.'}), 404

        cursor.execute("DELETE FROM Veiculos WHERE id_veiculo = ?", (id,))
        conn.commit()
        return jsonify({'mensagem': 'Veiculo deletado com sucesso!'}), 200

    except sqlite3.Error as e:
        return jsonify({'erro': f'Erro no banco de dados: {str(e)}'}), 500

    finally:
        if conn:
            conn.close()

##########################################################

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

@admin_bp.route("/relatorios", methods=["GET", "POST"])
def pagina_relatorios():
    motoristas = dados_relatorios()
    return render_template("relatorioAdmin.html", motoristas=motoristas)

#############################################################

######### Logs #########################
@admin_bp.route("/logs", methods=["GET", "POST"])
def pagina_logs():
    return render_template("logsAdmin.html")


########################## Adicionar Motoristas e Veiculos ##############

@admin_bp.route('/adicionar_motorista_veiculos', methods=['GET', 'POST'])
def adicionar_motorista():
    if request.method == 'POST':
        id_empresa = session.get('id_empresa')

        if not id_empresa:
            flash("Sessão inválida. Faça login novamente.", "erro")
            return redirect(url_for('exibir_login'))

        # MOTORISTA
        nome_motorista = request.form['nome_motorista']
        cpf = request.form['cpf']
        cnh = request.form['cnh']
        data_nascimento = request.form['data_nascimento']
        status_motorista = request.form['status-motorista']

        # VEÍCULO
        placa = request.form['placa']
        modelo = request.form['modelo']
        marca = request.form['marca']
        ano = request.form['ano']
        frota = request.form['frota']
        km_atual = request.form['km_atual']
        media_km_litro = request.form['media_km_litro']
        ultima_manutencao = request.form['ultima_manutencao']
        status_veiculo = request.form['status-veiculo']

        try:
            # 1. Adiciona motorista no banco e recupera ID
            id_motorista = adicionar_motorista_banco(nome_motorista, cpf, cnh, data_nascimento, status_motorista, id_empresa)

            # 2. Adiciona veículo vinculado ao motorista
            adicionar_veiculo_banco(
                placa, modelo, marca, ano, frota, km_atual, media_km_litro,
                ultima_manutencao, status_veiculo, id_motorista, id_empresa
            )

            flash("Motorista e veículo cadastrados com sucesso!", "sucesso")
            return redirect(url_for('admin.listar_motoristas'))

        except Exception as e:
            flash(f"Erro ao cadastrar: {str(e)}", "erro")

    return render_template('cadastro_motorista_veiculos.html')



########################## relatorio ##############################

from flask import jsonify
from database.admin_database.admin import dados_por_id_motorista

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
            data = d["data_chegada"]

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