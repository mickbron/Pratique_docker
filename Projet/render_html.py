from stats import displayStats
from product_card import createProductCard


def render_html(products, filename="product_list.html"):
    """
    Génère un fichier HTML avec les statistiques et la grille de produits.
    """
    stats_html = displayStats(products)
    cards_html = "\n".join(createProductCard(p) for p in products)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Liste des produits Odoo</title>
    <style>
        body {{
            margin: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #141e30, #243b55);
            color: #f5f5f5;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
        h1 {{ text-align: center; margin-bottom: 1rem; }}
        .stats {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 2rem;
            justify-content: center;
        }}
        .stat-card {{
            background: rgba(0, 0, 0, 0.2);
            padding: 1rem 1.5rem;
            border-radius: 0.75rem;
            backdrop-filter: blur(6px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            min-width: 200px;
            text-align: center;
        }}
        .stat-card h2 {{ margin: 0; font-size: 1rem; opacity: 0.8; }}
        .stat-card p {{ margin: 0.3rem 0 0; font-size: 1.4rem; font-weight: bold; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        .product-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 1rem;
            padding: 1.25rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.4);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .product-card:hover {{
            transform: translateY(-6px) scale(1.01);
            box-shadow: 0 16px 35px rgba(0,0,0,0.6);
        }}
        .product-name {{ margin: 0 0 0.3rem; font-size: 1.2rem; }}
        .product-type {{ margin: 0 0 0.75rem; opacity: 0.85; font-size: 0.9rem; }}
        .product-price {{ margin: 0 0 0.5rem; font-size: 1.1rem; font-weight: bold; }}
        .product-ref, .product-category, .product-stock {{
            margin: 0.2rem 0;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Produits Odoo</h1>
        <section class="stats">
            {stats_html}
        </section>
        <section class="grid">
            {cards_html}
        </section>
    </div>
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Page HTML générée : {filename}")
