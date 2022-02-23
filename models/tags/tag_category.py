from odoo import _, fields, models


class Category(models.Model):
    _name = "ayu_product_data.tag_category"
    _description = "Product Tag Category"
    _order = "sequence,name"

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

    use_as_filter = fields.Boolean(
        default=True,
    )

    tag_ids = fields.One2many(
        "ayu_product_data.tag",
        "category_id",
        string="Tags",
    )

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=_("%s (copy)") % (self.name or ""))
        return super().copy(default)
