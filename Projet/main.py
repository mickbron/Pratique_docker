from load_products import load_products
from render_html import render_html


if __name__ == "__main__":
    try:
        products = load_products()
        render_html(products)
    except Exception as e:
        print("[ERREUR]", e)
