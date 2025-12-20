from stats import displayStats
from product_card import createProductCard


def render_html(products=None, error_msg=None) -> str:
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
            <h2>Aucune propriété affichée</h2>
            <p>Clique sur <strong>Charger les produits</strong> pour afficher les produits depuis Odoo.</p>
        </div>
        """

    # Boutons bas de page seulement si on a des produits
    bottom_actions = ""
    if products:
        bottom_actions = """
        <div class="bottom-actions">
            <button class="btn btn-primary" type="submit">Créer la commande</button>
            <a class="btn" href="/orders" style="text-decoration:none;">Suivre les commandes</a>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Propriétés Odoo</title>
  <link rel="stylesheet" href="/static/style.css" />
</head>
<body>
  <div class="wrap">
    <header>
      <div class="title">
        <h1>Propriétés locatives</h1>
        <p class="subtitle">
          Interface dynamique (Flask → Odoo JSON-RPC). Clique sur le bouton pour recharger depuis Odoo.
        </p>
      </div>

      <div class="actions">
        <form method="POST" action="/load">
          <button class="btn btn-primary" type="submit" aria-label="Charger les produits">
            Charger les produits
          </button>
        </form>
        <a class="btn" href="/orders" style="text-decoration:none;">Suivi commandes</a>
      </div>
    </header>

    {error_html}

    <section class="stats">{stats_html}</section>

    {empty_state_html}

    <!-- Form de création de commande (checkbox + qty dans chaque carte) -->
    <form method="POST" action="/create-order">
      <section class="grid">
        {cards_html}
      </section>
      {bottom_actions}
    </form>

    <footer>Python (Flask) • Odoo JSON-RPC • Propriétés locatives • Commandes</footer>
  </div>
</body>
</html>
"""
