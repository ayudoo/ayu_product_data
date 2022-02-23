from odoo import _, fields, models


class ProductCondition(models.Model):
    _inherit = ["ayu_product_data.taggable"]
    _name = "ayu_product_data.condition"
    _description = "Product Condition"
    _order = "sequence, name"

    _sql_constraints = [
        ('unique_identifier', 'UNIQUE(identifier)', "The identifier already exists"),
    ]

    sequence = fields.Integer("Sequence")
    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )

    identifier = fields.Char(translate=False, required=True)
    name = fields.Char(translate=True, required=True)

    item_group_ids = fields.One2many(
        "ayu_product_data.item_group",
        "ayu_condition_id",
        string="Item Groups",
    )
    product_template_ids = fields.One2many(
        "product.template",
        "ayu_condition_id",
        string="Product Templates",
    )

    def copy(self, default=None):
        default = dict(default or {})
        default.update(
            name=_("%s (copy)") % (self.name or ''))
        return super().copy(default)
