from stats import displayStats
from product_card import createProductCard


def render_html(products=None, error_msg=None):
    products = products or []

    stats_html = displayStats(products) if products else ""
    cards_html = "\n".join(createProductCard(p) for p in products) if products else ""

    error_html = ""
    if error_msg:
        error_html = f"""
        <div class="alert alert-error" role="alert">
            <strong>Erreur :</strong> {error_msg}
        </div>
        """

    empty_state_html = ""
    if not products and not error_msg:
        empty_state_html = """
        <div class="empty">
            <h2>Aucun produit affiché</h2>
            <p>Clique sur <strong>Charger les produits</strong> pour récupérer les produits depuis Odoo.</p>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Produits Odoo</title>

  <style>
    :root {{
      --bg1: #0b1220;
      --bg2: #101b33;
      --card: rgba(255,255,255,0.06);
      --card2: rgba(0,0,0,0.25);
      --text: #eaf0ff;
      --muted: rgba(234,240,255,0.75);
      --border: rgba(234,240,255,0.14);
      --shadow: 0 14px 30px rgba(0,0,0,0.35);
      --radius: 18px;

      --ok: #22c55e;
      --ok2: #16a34a;
      --danger: #ef4444;
      --dangerBg: rgba(239,68,68,0.16);
    }}

    * {{ box-sizing: border-box; }}
    html, body {{ height: 100%; }}
    body {{
      margin: 0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      color: var(--text);
      background: radial-gradient(1200px 600px at 20% 0%, #1a2a55 0%, transparent 60%),
                  radial-gradient(900px 500px at 80% 10%, #2a1a55 0%, transparent 55%),
                  linear-gradient(135deg, var(--bg1), var(--bg2));
    }}

    .wrap {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 28px 16px 60px;
    }}

    header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
      margin-bottom: 18px;
    }}

    .title {{
      display: grid;
      gap: 6px;
    }}

    h1 {{
      margin: 0;
      font-size: clamp(22px, 3vw, 32px);
      letter-spacing: 0.2px;
    }}

    .subtitle {{
      margin: 0;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.4;
    }}

    .actions {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .btn {{
      appearance: none;
      border: 1px solid rgba(255,255,255,0.14);
      background: linear-gradient(180deg, rgba(255,255,255,0.10), rgba(255,255,255,0.06));
      color: var(--text);
      padding: 11px 14px;
      border-radius: 12px;
      cursor: pointer;
      font-weight: 700;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 10px 22px rgba(0,0,0,0.25);
      transition: transform 0.12s ease, filter 0.12s ease, border-color 0.12s ease;
      user-select: none;
    }}

    .btn:hover {{
      transform: translateY(-1px);
      filter: brightness(1.03);
      border-color: rgba(255,255,255,0.22);
    }}

    .btn-primary {{
      background: linear-gradient(180deg, rgba(34,197,94,0.95), rgba(22,163,74,0.95));
      border-color: rgba(34,197,94,0.25);
      color: #06210f;
      box-shadow: 0 12px 26px rgba(34,197,94,0.15);
    }}

    .btn-primary:hover {{
      filter: brightness(1.02);
    }}

    .btn svg {{
      width: 18px;
      height: 18px;
      flex: 0 0 auto;
    }}

    .alert {{
      padding: 12px 14px;
      border-radius: 14px;
      border: 1px solid var(--border);
      background: var(--card2);
      box-shadow: var(--shadow);
      margin: 14px 0 18px;
    }}

    .alert-error {{
      border-color: rgba(239,68,68,0.35);
      background: var(--dangerBg);
    }}

    .stats {{
      display: flex;
      flex-wrap: wrap;
      gap: 14px;
      margin: 18px 0 20px;
    }}

    /* Les stat-cards viennent de displayStats() */
    .stat-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 14px 16px;
      min-width: 220px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(6px);
    }}
    .stat-card h3 {{
      margin: 0 0 8px;
      font-size: 13px;
      color: var(--muted);
      letter-spacing: 0.2px;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .stat-card p {{
      margin: 0;
      font-size: 22px;
      font-weight: 800;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 14px;
    }}

    /* Style de base des product-cards (si product_card.py n'en met pas) */
    .product-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(6px);
      transition: transform 0.12s ease, border-color 0.12s ease;
    }}

    .product-card:hover {{
      transform: translateY(-2px);
      border-color: rgba(234,240,255,0.22);
    }}

    .empty {{
      margin-top: 18px;
      padding: 18px;
      background: var(--card);
      border: 1px dashed rgba(234,240,255,0.25);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }}

    .empty h2 {{
      margin: 0 0 6px;
      font-size: 18px;
    }}

    .empty p {{
      margin: 0;
      color: var(--muted);
      line-height: 1.5;
    }}

    footer {{
      margin-top: 26px;
      color: var(--muted);
      font-size: 12px;
      text-align: center;
    }}

    /* Responsive petit écran */
    @media (max-width: 520px) {{
      .btn {{
        width: 100%;
        justify-content: center;
      }}
      .stat-card {{
        min-width: 0;
        flex: 1 1 100%;
      }}
    }}
  </style>
</head>

<body>
  <div class="wrap">
    <header>
      <div class="title">
        <h1>Produits Odoo</h1>
        <p class="subtitle">
          Clique sur <strong>Charger les produits</strong> pour récupérer les produits depuis Odoo.
          (Ajoute un produit puis recharge pour le voir apparaître.)
        </p>
      </div>

      <div class="actions">
        <form method="POST" action="/load">
          <button class="btn btn-primary" type="submit" aria-label="Charger les produits">
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M12 3v8m0 0l3-3m-3 3L9 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M5 14v4a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Charger les produits
          </button>
        </form>
      </div>
    </header>

    {error_html}

    <section class="stats">
      {stats_html}
    </section>

    {empty_state_html}

    <section class="grid">
      {cards_html}
    </section>

    <footer>
      Serveur Python (Flask) → API Odoo JSON-RPC • Interface responsive
    </footer>
  </div>
</body>
</html>
"""
