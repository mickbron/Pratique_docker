from flask import Flask, Response, request
import base64

from load_products import load_products
from render_html import render_html
from call_odoo import call_odoo
from odoo_config import authenticate
from order_service import create_sale_order, list_sale_orders, get_sale_order

app = Flask(__name__)


@app.get("/")
def home():
    return render_html()


@app.post("/load")
def load():
    try:
        products = load_products()
        return render_html(products)
    except Exception as e:
        return render_html(error_msg=str(e))


@app.get("/product-image/<int:product_id>")
def product_image(product_id: int):
    try:
        authenticate()
        res = call_odoo("product.template", "read", [[product_id], ["image_512"]], {})
        if not res or not res[0].get("image_512"):
            svg = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="480">
              <rect width="100%" height="100%" fill="#334155"/>
              <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
                    fill="#eaf0ff" font-size="28" font-family="Arial">
                Pas d'image
              </text></svg>"""
            return Response(svg, mimetype="image/svg+xml")

        img_bytes = base64.b64decode(res[0]["image_512"])
        return Response(img_bytes, mimetype="image/jpeg")
    except Exception:
        svg = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="480">
          <rect width="100%" height="100%" fill="#7f1d1d"/>
          <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
                fill="#fff" font-size="22" font-family="Arial">
            Erreur image
          </text></svg>"""
        return Response(svg, mimetype="image/svg+xml")


@app.post("/create-order")
def create_order():
    try:
        products = load_products()

        items = []
        for p in products:
            pid = int(p["id"])
            checked = request.form.get(f"pid_{pid}")  # "on" si coché
            if not checked:
                continue
            qty_str = request.form.get(f"qty_{pid}", "1")
            qty = float(qty_str) if qty_str else 1.0
            items.append({"product_id": pid, "qty": qty})

        order_id = create_sale_order(items)
        order = get_sale_order(order_id)
        return render_order_detail_html(order)

    except Exception as e:
        # Réaffiche page produits avec erreur
        products = load_products()
        return render_html(products, error_msg=str(e))


@app.get("/orders")
def orders():
    orders_list = list_sale_orders(limit=50)
    return render_orders_list_html(orders_list)


@app.get("/order/<int:order_id>")
def order_detail(order_id: int):
    order = get_sale_order(order_id)
    return render_order_detail_html(order)


def render_orders_list_html(orders_list: list[dict]) -> str:
    rows = ""
    for o in orders_list:
        oid = o.get("id", "")
        rows += f"""
        <tr>
          <td><a href="/order/{oid}" style="color:#eaf0ff;">{o.get('name','')}</a></td>
          <td><span class="badge">{o.get('state','')}</span></td>
          <td>{o.get('amount_total','')}</td>
          <td>{o.get('create_date','')}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="fr"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Suivi commandes</title>
<link rel="stylesheet" href="/static/style.css"/>
</head><body>
<div class="wrap">
  <header>
    <div class="title">
      <h1>Suivi des commandes</h1>
      <p class="subtitle">Liste des dernières commandes créées.</p>
    </div>
    <div class="actions">
      <a class="btn" href="/" style="text-decoration:none;">← Retour</a>
    </div>
  </header>

  <table class="table">
    <thead>
      <tr><th>Commande</th><th>État</th><th>Total</th><th>Date</th></tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>

  <footer>Page de suivi (liste)</footer>
</div>
</body></html>"""


def render_order_detail_html(order: dict) -> str:
    oid = order.get("id", "")
    name = order.get("name", "")
    state = order.get("state", "")
    total = order.get("amount_total", 0)
    untaxed = order.get("amount_untaxed", 0)
    tax = order.get("amount_tax", 0)

    line_rows = ""
    for l in order.get("lines", []):
        prod = l.get("product_id")
        prod_name = prod[1] if isinstance(prod, list) and len(prod) >= 2 else ""
        qty = l.get("product_uom_qty", 0)
        pu = l.get("price_unit", 0)
        sub = l.get("price_subtotal", 0)
        line_rows += f"<tr><td>{prod_name}</td><td>{qty}</td><td>{pu}</td><td>{sub}</td></tr>"

    return f"""<!DOCTYPE html>
<html lang="fr"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Détail commande {name}</title>
<link rel="stylesheet" href="/static/style.css"/>
</head><body>
<div class="wrap">
  <header>
    <div class="title">
      <h1>{name}</h1>
      <p class="subtitle">État : <span class="badge">{state}</span></p>
    </div>
    <div class="actions">
      <a class="btn" href="/orders" style="text-decoration:none;">← Liste</a>
      <a class="btn btn-primary" href="/order/{oid}" style="text-decoration:none;">Rafraîchir</a>
    </div>
  </header>

  <table class="table">
    <thead><tr><th>Produit</th><th>Qté</th><th>PU</th><th>Sous-total</th></tr></thead>
    <tbody>{line_rows}</tbody>
  </table>

  <div style="margin-top:16px; display:flex; flex-wrap:wrap; gap:14px;">
    <div class="stat-card" style="min-width:220px;"><h3>Total HT</h3><p>{untaxed}</p></div>
    <div class="stat-card" style="min-width:220px;"><h3>Taxes</h3><p>{tax}</p></div>
    <div class="stat-card" style="min-width:220px;"><h3>Total TTC</h3><p>{total}</p></div>
  </div>

  <footer>Page de suivi (détail)</footer>
</div>
</body></html>"""
