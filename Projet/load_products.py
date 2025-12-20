from odoo_config import authenticate
from call_odoo import call_odoo


def load_products():
    authenticate()

    fields = [
        # nécessaire pour construire l’URL image
        "id",

        # Champs standards
        "name",
        "list_price",
        "type",
        "default_code",
        "categ_id",

        # Rental info
        "max_guests",
        "beds",
        "bedrooms",
        "bathrooms",

        # Adresse
        "street",
        "number",
        "postal_code",

        # Amenities
        "air_conditioning_available",
        "terrace_available",
        "garden_available",
        "pool_available",
        "hot_tub_available",
        "ev_charger_available",
        "indoor_fireplace_available",
        "outdoor_fireplace_available",
        "dedicated_workspace_available",
        "gym_available",

        # Accessibilité
        "toilet_grab_bar_available",
        "shower_grab_bar_available",
        "step_free_shower_available",
        "shower_bath_chair_available",
        "step_free_bedroom_access_available",
        "wide_bedroom_entrance_available",
        "step_free_access_available",
    ]

    # Filtre propriétés locatives (6.4)
    domain = []

    kwargs = {
        "domain": domain,
        "fields": fields,
        "limit": 50,
    }

    return call_odoo("product.template", "search_read", [], kwargs)
