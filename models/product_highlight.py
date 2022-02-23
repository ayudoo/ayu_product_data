from odoo import _, fields, models


class ProductHighlight(models.Model):
    _inherit = ["ayu_product_data.taggable"]
    _name = "ayu_product_data.product_highlight"
    _description = "Product Highlight"
    _order = "name"

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "This highlight already exists"),
    ]

    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )
    name = fields.Char(string="Content", translate=True)

    item_group_ids = fields.Many2many(
        "ayu_product_data.item_group",
        relation="ayu_product_data_item_group_product_highlight_rel",
        column1="product_highlight_id",
        column2="item_group_id",
        string="Item Groups",
    )

    product_template_ids = fields.Many2many(
        "product.template",
        relation="ayu_product_data_product_template_highlight_rel",
        column1="product_highlight_id",
        column2="product_template_id",
        string="Product Templates",
    )

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=_("%s (copy)") % (self.name or ""))
        return super().copy(default)
