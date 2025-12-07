from functools import reduce


def displayStats(products):
    total_products = len(products)

    total_price = reduce(
        lambda acc, p: acc + float(p.get("list_price") or 0),
        products,
        0,
    )

    average_price = total_price / total_products if total_products > 0 else 0

    types = set(p.get("type") for p in products if p.get("type"))
    unique_type_count = len(types)

    return f"""
        <div class="stat-card">
            <h2>Nombre de produits</h2>
            <p>{total_products}</p>
        </div>
        <div class="stat-card">
            <h2>Prix moyen</h2>
            <p>{average_price:.2f} €</p>
        </div>
        <div class="stat-card">
            <h2>Nombre de types</h2>
            <p>{unique_type_count}</p>
        </div>
    """
