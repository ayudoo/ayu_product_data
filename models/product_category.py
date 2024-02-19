from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = ["product.category", "ayu_product_data.taggable"]
    _name = "product.category"

    def _compute_product_type_name(self):
        for record in self:
            if record.parent_id:
                record.product_type_name = '%s > %s' % (
                    record.parent_id.product_type_name, record.name,
                )
            else:
                record.product_type_name = record.name

    product_type_name = fields.Char(
        string="The name in the Google product_type format, separated by '>'",
        compute=_compute_product_type_name,
    )

    def _get_product_templates_to_update(self):
        # note, we do not add tags to child categories here
        return self.env['product.template'].search([("categ_id", "in", self.ids)])
