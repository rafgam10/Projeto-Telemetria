import requests

def verificar_placa_no_servidor(placa):
    response = requests.get(f"http://127.0.0.1:5000/api/placas")
    if response.status_code == 200:
        placas = response.json()["placas"]
        return placa.upper() in placas
    return False
