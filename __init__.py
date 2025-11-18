from . import controllers, models, report


def init_google_categories(env):
    env["ayu_product_data.google_category"]._init_google_categories()
