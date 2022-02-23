from odoo import _, fields, models


class ProductLine(models.Model):
    _inherit = ["ayu_product_data.taggable"]
    _name = "ayu_product_data.line"
    _description = "Product Line"
    _order = "sequence, name"

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name already exists"),
    ]

    sequence = fields.Integer("Sequence")
    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )

    name = fields.Char(translate=True, required=True)
    description = fields.Char(translate=True)

    item_group_ids = fields.One2many(
        "ayu_product_data.item_group",
        "ayu_line_id",
        string="Item Groups",
    )
    product_template_ids = fields.One2many(
        "product.template",
        "ayu_line_id",
        string="Product Templates",
    )

    detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        relation="ayu_product_data_line_detail_rel",
        column1="line_id",
        column2="product_detail_id",
        string="Product Details",
    )

    def get_product_details(self):
        return self.detail_ids

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=_("%s (copy)") % (self.name or ""))
        return super().copy(default)
