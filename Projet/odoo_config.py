import requests
import random

ODOO_URL = "http://localhost:8069"
DB = "mickbronBD"
USERNAME = "mickbron20@gmail.com"
PASSWORD = "Dockermick@20"

session = requests.Session()
uid = None
session_id = None


def authenticate():
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

    response = session.post(f"{ODOO_URL}/web/session/authenticate", json=payload)
    response.raise_for_status()
    data = response.json()

    if "error" in data or not data.get("result", {}).get("uid"):
        raise Exception("Authentification Odoo échouée")

    uid = data["result"]["uid"]
    session_id = session.cookies.get("session_id")

