from type_labels import get_type_label


def createProductCard(p):
    name = p.get("name", "Sans nom")
    price = p.get("list_price") or 0
    ref = p.get("default_code") or "N/A"
    type_label = get_type_label(p.get("type"))

    categ = p.get("categ_id")
    categ_name = categ[1] if isinstance(categ, list) else "Sans catégorie"

    return f"""
    <div class="product-card">
        <h3>{name}</h3>
        <p>{type_label}</p>
        <p><strong>{price:.2f} €</strong></p>
        <p>Réf : {ref}</p>
        <p>{categ_name}</p>
    </div>
    """
