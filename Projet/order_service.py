from call_odoo import call_odoo
from odoo_config import authenticate


def get_or_create_default_customer() -> int:
    """
    Retourne un partner_id client.
    - Cherche 'Web Customer'
    - Sinon le crée
    """
    authenticate()

    partners = call_odoo(
        "res.partner",
        "search_read",
        [],
        {"domain": [["name", "=", "Web Customer"]], "fields": ["id", "name"], "limit": 1},
    )

    if partners:
        return int(partners[0]["id"])

    # ✅ create(vals) -> vals doit être dans args
    partner_id = call_odoo(
        "res.partner",
        "create",
        [{"name": "Web Customer", "customer_rank": 1}],
        {},
    )
    return int(partner_id)


def create_sale_order(items: list[dict]) -> int:
    """
    Crée une commande Odoo (sale.order) avec lignes.
    items: [{"product_id": int, "qty": float}, ...]
    Retourne l'ID de la commande.
    """
    authenticate()

    if not items:
        raise Exception("Aucun produit sélectionné.")

    partner_id = get_or_create_default_customer()

    # Construire les lignes: (0,0, {...}) = création d'une ligne
    order_lines = []
    for it in items:
        pid = int(it["product_id"])
        qty = float(it["qty"])
        if qty <= 0:
            continue
        order_lines.append((0, 0, {"product_id": pid, "product_uom_qty": qty}))

    if not order_lines:
        raise Exception("Quantités invalides (tout est à 0).")

    vals = {
        "partner_id": partner_id,
        "order_line": order_lines,
    }

    # ✅ create(vals) -> vals doit être dans args
    order_id = call_odoo(
        "sale.order",
        "create",
        [vals],
        {},
    )
    return int(order_id)


def list_sale_orders(limit: int = 50) -> list[dict]:
    authenticate()
    return call_odoo(
        "sale.order",
        "search_read",
        [],
        {
            "domain": [],
            "fields": ["id", "name", "state", "amount_total", "create_date"],
            "limit": limit,
            "order": "id desc",
        },
    )


def get_sale_order(order_id: int) -> dict:
    authenticate()

    orders = call_odoo(
        "sale.order",
        "read",
        [[order_id], ["id", "name", "state", "amount_total", "amount_untaxed", "amount_tax", "create_date", "order_line"]],
        {},
    )
    if not orders:
        raise Exception("Commande introuvable.")
    order = orders[0]

    line_ids = order.get("order_line", [])
    lines = []
    if line_ids:
        lines = call_odoo(
            "sale.order.line",
            "read",
            [line_ids, ["product_id", "product_uom_qty", "price_unit", "price_subtotal"]],
            {},
        )

    order["lines"] = lines
    return order
