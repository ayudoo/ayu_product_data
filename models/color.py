from odoo import _, api, fields, models
from odoo.exceptions import UserError

COLOR_IMAGE_SIZE = (30, 30)


class Color(models.Model):
    _inherit = ["ayu_product_data.taggable"]
    _name = "ayu_product_data.color"
    _description = "Color"
    _order = "sequence, identifier"
    # _rec_name = "display_name"

    _sql_constraints = [
        ("unique_identifier", "UNIQUE(identifier)", "The identifier already exists"),
    ]

    sequence = fields.Integer("Sequence")
    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )

    identifier = fields.Char(translate=False, required=True)
    name = fields.Char(translate=True, required=True)

    html_color = fields.Char(
        string="Color Index",
        help="You can set a specific HTML color index (e.g. #ff0000).",
    )

    color_image = fields.Image(
        string="Color Image",
        help="You can use an image for the color."
        + " It will be converted to {}px".format(
            "x".join([str(x) for x in COLOR_IMAGE_SIZE])
        ),
        max_width=COLOR_IMAGE_SIZE[0],
        max_height=COLOR_IMAGE_SIZE[1],
    )

    bright_color = fields.Boolean(
        string="Bright Color",
        default=False,
        help="Helper field to make the color select more visible for bright colors.",
    )

    item_group_ids = fields.One2many(
        "ayu_product_data.item_group",
        "ayu_color_id",
        string="Item Groups",
    )
    product_template_ids = fields.One2many(
        "product.template",
        "ayu_color_id",
        string="Product Templates",
    )

    detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        relation="ayu_product_data_color_detail_rel",
        column1="color_id",
        column2="product_detail_id",
        string="Product Details",
    )

    def get_product_details(self):
        return self.detail_ids

    @api.depends("name", "identifier")
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.identifier} {record.name}"

    @api.model
    def name_create(self, name):
        try:
            identifier, name = name.split(" ", 1)
        except ValueError:
            raise UserError("For quick create, please use this format, separated by space: <identifier> <color name>")

        record = self.create(
            {
                "identifier": identifier,
                "name": name,
            }
        )
        return record.id, record.display_name

    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None, order=None,
    ):
        tail = False
        identifier = name.split(" ", 1)
        if len(identifier) == 1:
            identifier = identifier[0]
        else:
            identifier, tail = identifier

        domain = [
            ("|"),
            ("identifier", "=ilike", identifier + "%"),
            ("name", operator, identifier),
        ]
        if tail:
            domain = [("name", operator, tail)] + domain

        if args:
            domain = args + domain

        return self._search(domain, limit=limit, access_rights_uid=name_get_uid, order=order)

    def copy(self, default=None):
        default = dict(default or {})
        default.update(identifier=_("%s (copy)") % (self.identifier or ""))
        return super().copy(default)
