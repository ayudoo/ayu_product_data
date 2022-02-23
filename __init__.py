from odoo import api, SUPERUSER_ID
from . import controllers, models, report


def init_google_categories(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ayu_product_data.google_category"]._init_google_categories()
