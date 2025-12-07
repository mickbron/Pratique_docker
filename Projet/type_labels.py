TYPE_LABELS = {
    "product": "Stockable",
    "consu": "Consommable",
    "service": "Service",
}


def get_type_label(ptype):
    return TYPE_LABELS.get(ptype, ptype or "Inconnu")
