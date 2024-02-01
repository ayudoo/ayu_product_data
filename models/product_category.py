from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = ["product.category", "ayu_product_data.taggable"]
    _name = "product.category"

    def _get_product_templates_to_update(self):
        # note, we do not add tags to child categories here
        return self.env['product.template'].search([("categ_id", "in", self.ids)])
