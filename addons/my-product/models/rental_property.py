from odoo import models, fields

class RentalProperty(models.Model):
    _inherit = 'product.template'

    max_guests = fields.Integer('Nombre maximum invités')
    beds = fields.Integer('Nombre de lits')
    bedrooms = fields.Integer('Nombre de chambres')
    bathrooms = fields.Integer('Nombre de salles de bain')
    street = fields.Char('Rue')
    number = fields.Char('Numéro')
    postal_code = fields.Char('Code postal')
    toilet_grab_bar_available = fields.Boolean('Barre appui pour toilettes')

    # Amenity fields
    air_conditioning_available = fields.Boolean('Climatisation')
    terrace_available = fields.Boolean('Terrasse')
    garden_available = fields.Boolean('Jardin')
    pool_available = fields.Boolean('Piscine')
    hot_tub_available = fields.Boolean('Jacuzzi')
    ev_charger_available = fields.Boolean('Chargeur EV')
    indoor_fireplace_available = fields.Boolean('Cheminée intérieure')
    outdoor_fireplace_available = fields.Boolean('Cheminée extérieure')
    dedicated_workspace_available = fields.Boolean('Espace de travail dédié')
    gym_available = fields.Boolean('Salle de sport')

    # Accessibility fields
    shower_grab_bar_available = fields.Boolean('Barre appui de douche')
    step_free_shower_available = fields.Boolean('Douche sans marche')
    shower_bath_chair_available = fields.Boolean('Chaise de douche/baignoire')
    step_free_bedroom_access_available = fields.Boolean('Accès sans marche à la chambre')
    wide_bedroom_entrance_available = fields.Boolean('Entrée large de chambre')
    step_free_access_available = fields.Boolean('Accès sans marche général')
