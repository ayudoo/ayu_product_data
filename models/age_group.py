from odoo import fields, models, _


class AgeGroup(models.Model):
    _inherit = ["ayu_product_data.taggable"]
    _name = "ayu_product_data.age_group"
    _description = "Age Group"
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
    description = fields.Char(translate=True)

    item_group_ids = fields.One2many(
        "ayu_product_data.item_group",
        "ayu_age_group_id",
        string="Item Groups",
    )
    product_template_ids = fields.One2many(
        "product.template",
        "ayu_age_group_id",
        string="Product Templates",
    )

    def copy(self, default=None):
        default = dict(default or {})
        default.update(
            name=_("%s (copy)") % (self.name or ''))
        return super().copy(default)
