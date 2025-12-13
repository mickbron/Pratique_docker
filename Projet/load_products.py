from odoo_config import authenticate
from call_odoo import call_odoo


def load_products():
    authenticate()

    fields = ["name", "list_price", "type", "default_code", "categ_id"]

    kwargs = {
        "domain": [],
        "fields": fields,
        "limit": 50,
    }

    return call_odoo("product.template", "search_read", [], kwargs)
