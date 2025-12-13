import random
import odoo_config


def call_odoo(model, method, args=None, kwargs=None):
    if odoo_config.uid is None:
        raise Exception("Non authentifié")

    args = args or []
    kwargs = kwargs or {}

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

    response = odoo_config.session.post(
        f"{odoo_config.ODOO_URL}/web/dataset/call_kw", json=payload
    )
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        raise Exception(data["error"])

    return data.get("result")
