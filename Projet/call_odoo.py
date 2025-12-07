import random
import odoo_config


def call_odoo(model, method, args=None, kwargs=None):
    if odoo_config.uid is None or odoo_config.session_id is None:
        raise Exception("Non authentifié : appelle d'abord authenticate().")

    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": model,
            "method": method,
            "args": args,
            "kwargs": kwargs,
        },
        "id": random.randint(1, 1_000_000),
    }

    url = f"{odoo_config.ODOO_URL}/web/dataset/call_kw"
    response = odoo_config.session.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise Exception(f"Erreur Odoo lors de l'appel à {model}.{method} : {data['error']}")

    return data.get("result")
