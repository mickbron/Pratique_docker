from type_labels import get_type_label


def _badge(icon: str, label: str) -> str:
    return f"<span class='equip-badge'>{icon} {label}</span>"


def createProductCard(p):
    product_id = int(p.get("id") or 0)

    name = p.get("name", "Sans nom")
    price = float(p.get("list_price") or 0.0)
    ref = p.get("default_code") or "N/A"
    type_label = get_type_label(p.get("type"))

    categ = p.get("categ_id")
    categ_name = categ[1] if isinstance(categ, list) and len(categ) >= 2 else "Sans catégorie"

    # Image (proxy Flask)
    img_html = ""
    if product_id:
        img_html = f"""
        <div class="product-image-wrap">
            <img class="product-image" src="/product-image/{product_id}" alt="Image {name}">
        </div>
        """

    # Bloc sélection commande
    order_pick_html = ""
    if product_id:
        order_pick_html = f"""
        <div class="order-pick">
            <label class="pick">
                <input type="checkbox" name="pid_{product_id}" />
                Ajouter
            </label>
            <label class="qty">
                Qté:
                <input type="number" min="1" step="1" name="qty_{product_id}" value="1" />
            </label>
        </div>
        """

    # Rental info
    max_guests = int(p.get("max_guests") or 0)
    beds = int(p.get("beds") or 0)
    bedrooms = int(p.get("bedrooms") or 0)
    bathrooms = int(p.get("bathrooms") or 0)

    # Adresse
    street = p.get("street") or ""
    number = p.get("number") or ""
    postal_code = p.get("postal_code") or ""
    address_parts = [part for part in [street, number, postal_code] if part]
    address = " ".join(address_parts) if address_parts else "Adresse non renseignée"

    # Amenities
    amenities = [
        ("pool_available", "🏊", "Piscine"),
        ("hot_tub_available", "🛁", "Jacuzzi"),
        ("air_conditioning_available", "❄️", "Climatisation"),
        ("terrace_available", "🌿", "Terrasse"),
        ("garden_available", "🌳", "Jardin"),
        ("ev_charger_available", "🔌", "Chargeur EV"),
        ("indoor_fireplace_available", "🔥", "Cheminée int."),
        ("outdoor_fireplace_available", "🔥", "Cheminée ext."),
        ("dedicated_workspace_available", "💻", "Espace travail"),
        ("gym_available", "🏋️", "Salle de sport"),
    ]

    # Accessibilité
    accessibility = [
        ("toilet_grab_bar_available", "🧻", "Barre appui WC"),
        ("shower_grab_bar_available", "🚿", "Barre appui douche"),
        ("step_free_shower_available", "🦽", "Douche sans marche"),
        ("shower_bath_chair_available", "🪑", "Chaise douche/baignoire"),
        ("step_free_bedroom_access_available", "🛏️", "Accès chambre sans marche"),
        ("wide_bedroom_entrance_available", "🚪", "Entrée chambre large"),
        ("step_free_access_available", "✅", "Accès sans marche"),
    ]

    rental_info_html = ""
    if max_guests > 0:
        amen_badges = [_badge(icon, label) for field, icon, label in amenities if bool(p.get(field))]
        acc_badges = [_badge(icon, label) for field, icon, label in accessibility if bool(p.get(field))]

        amenities_html = "".join(amen_badges) if amen_badges else "<span class='muted'>Aucun équipement renseigné</span>"
        accessibility_html = "".join(acc_badges) if acc_badges else "<span class='muted'>Aucune info accessibilité</span>"

        rental_info_html = f"""
        <div class="rental-info">
            <div class="rental-row">
                <span>👥 <strong>{max_guests}</strong> invités</span>
                <span>🛏 <strong>{beds}</strong> lits • <strong>{bedrooms}</strong> chambres</span>
                <span>🛁 <strong>{bathrooms}</strong> sdb</span>
            </div>

            <div class="meta" style="margin-top:8px;">
                <div><span class="muted">Adresse</span> : {address}</div>
            </div>

            <div class="equipment">
                <div class="equip-section">
                    <div class="equip-title">Équipements</div>
                    <div class="equip-list">{amenities_html}</div>
                </div>
                <div class="equip-section">
                    <div class="equip-title">Accessibilité</div>
                    <div class="equip-list">{accessibility_html}</div>
                </div>
            </div>
        </div>
        """

    return f"""
    <div class="product-card">
        {img_html}

        <div class="card-top">
            <h3 class="product-name">{name}</h3>
            <div class="chip">{type_label}</div>
        </div>

        <div class="price">{price:.2f} € <span class="muted">/ nuit</span></div>

        <div class="meta">
            <div><span class="muted">Réf</span> : {ref}</div>
            <div><span class="muted">Catégorie</span> : {categ_name}</div>
        </div>

        {order_pick_html}

        {rental_info_html}
    </div>
    """
