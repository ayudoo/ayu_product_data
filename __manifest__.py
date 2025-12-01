# Copyright 2022 <mj@ayudoo.bg>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

{
    "author": "Michael Jurke, Ayudoo EOOD",
    "name": "Product Data, Tags and Feed",
    "summary": "Product Data Management with Tags and Feed",
    "description": """
Features:

* use sophisticated, reusable data fields to enrich your products with information
* export your data for your advertising partners
* group product templates by using an item group id with more flexibility than variants
* use flexible color images to present your products
* customize labels and periodically update your export data
* add product texts and attachments and show them in the product's page
    """,
    "version": "0.1",
    "license": "LGPL-3",
    "category": "Sales/Sales",
    "support": "support@ayudoo.bg",
    "depends": [
        "base",
        # product dependency by sale, payment, account
        "website_sale_stock",
        # absolutely not happy with this dependency, but to incorporate
        # country_of_origin, we have to.
        "stock_delivery",
    ],
    "data": [
        "security/product_data_security.xml",
        "security/ir.model.access.csv",
        "data/product_text_data.xml",
        "data/age_group_data.xml",
        "data/condition_data.xml",
        "data/gender_data.xml",
        "data/tag_category_data.xml",
        "data/ir_cron.xml",
        "views/age_group_view.xml",
        "views/condition_view.xml",
        "views/gender_view.xml",
        "views/google_category_view.xml",
        "views/product_template_view.xml",
        "views/item_group_view.xml",
        "views/line_view.xml",
        "views/color_view.xml",
        "views/material_view.xml",
        "views/product_category_view.xml",
        "views/product_detail_view.xml",
        "views/product_highlight_view.xml",
        "views/product_text_view.xml",
        "views/product_text_category_view.xml",
        "views/public_category_view.xml",
        "views/feed_view.xml",
        "views/tag_view.xml",
        "views/tag_category_view.xml",
        "views/templates.xml",
        "views/user_document_view.xml",
        "data/ir_exports_data.xml",
        "views/res_config_settings_view.xml",
        "report/sale_report_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "ayu_product_data/static/src/scss/backend.scss",
        ],
        "web.assets_frontend": [
            "ayu_product_data/static/src/scss/frontend.scss",
            # "ayu_product_data/static/src/js/product_color_select.js",
        ],
    },
    "application": True,
    "installable": True,
    "post_init_hook": "init_google_categories",
    "demo": [],
}
