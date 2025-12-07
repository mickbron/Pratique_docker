import requests
import random

# === Configuration Odoo ===
ODOO_URL = "http://localhost:8069"
DB = "mickbronBD"
USERNAME = "mickbron20@gmail.com"
PASSWORD = "Dockermick@20"

# === Session & identifiants Odoo ===
session = requests.Session()
uid = None
session_id = None


def authenticate():
    """
    Authentifie l'utilisateur auprès d'Odoo via JSON-RPC.
    Met à jour uid et session_id.
    """
    global uid, session_id

    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "db": DB,
            "login": USERNAME,
            "password": PASSWORD,
        },
        "id": random.randint(1, 1_000_000),
    }

    url = f"{ODOO_URL}/web/session/authenticate"
    response = session.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise Exception(f"Erreur d'authentification Odoo : {data['error']}")

    result = data.get("result")
    if not result:
        raise Exception("Réponse d'authentification invalide.")

    uid_value = result.get("uid")
    if not uid_value:
        raise Exception("Authentification échouée : uid manquant.")

    uid = uid_value
    session_id = session.cookies.get("session_id")

    print(f"[AUTH OK] uid = {uid}, session_id = {session_id}")
