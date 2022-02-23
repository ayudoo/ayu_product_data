from odoo import fields, models


class ProductPublicCategory(models.Model):
    _inherit = ["product.public.category", "ayu_product_data.taggable"]
    _name = "product.public.category"

    def _compute_product_type_name(self):
        for record in self:
            record.product_type_name = " > ".join(
                [c.name.replace(",", r"\,") for c in record.parents_and_self]
            )

    product_type_name = fields.Char(
        string="The name in the Google product_type format, separated by '>'",
        compute=_compute_product_type_name,
    )

    def _get_product_templates_to_update(self):
        return self.product_tmpl_ids
