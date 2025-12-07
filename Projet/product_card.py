from type_labels import get_type_label


def createProductCard(product):
    name = product.get("name", "Sans nom")
    list_price = product.get("list_price") or 0
    type_label = get_type_label(product.get("type"))
    default_code = product.get("default_code") or "N/A"

    categ = product.get("categ_id")
    categ_name = categ[1] if isinstance(categ, list) else "Sans catégorie"

    return f"""
    <div class="product-card">
        <h3 class="product-name">{name}</h3>
        <p class="product-type">{type_label}</p>
        <p class="product-price">{list_price:.2f} €</p>
        <p><strong>Réf :</strong> {default_code}</p>
        <p><strong>Catégorie :</strong> {categ_name}</p>
    </div>
    """
