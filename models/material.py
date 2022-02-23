from odoo import _, fields, models


class Material(models.Model):
    _inherit = ["ayu_product_data.taggable"]
    _name = "ayu_product_data.material"
    _description = "Material"
    _order = "name"

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name already exists"),
    ]

    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )

    name = fields.Char(translate=True)

    item_group_ids = fields.One2many(
        "ayu_product_data.item_group",
        "ayu_material_id",
        string="Item Groups",
    )
    product_template_ids = fields.One2many(
        "product.template",
        "ayu_material_id",
        string="Product Templates",
    )

    detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        relation="ayu_product_data_material_detail_rel",
        column1="material_id",
        column2="product_detail_id",
        string="Product Details",
    )

    def get_product_details(self):
        return self.detail_ids

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=_("%s (copy)") % (self.name or ""))
        return super().copy(default)
