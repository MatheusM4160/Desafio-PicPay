import requests
import sqlite3

def send_notification(to, message):
    url = "https://util.devi.tools/api/v1/notify"
    payload = {"to": to, "message": message}
    print(payload)

    try:
        response = requests.post(url, json=payload, timeout=5)  # 5 segundos de timeout
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Lidar com falha no envio (serviço indisponível, erro de conexão, etc.)
        print(f"Erro ao enviar notificação: {e}")
        return None

Id_Client = 1
Value = 50

with sqlite3.connect('register.db') as conn:
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM client WHERE id = ?""", (Id_Client,))
    result = cursor.fetchone()[3]
    send_notification(result, f'Você recebeu um pagamento de R${float(Value):.2f}!')