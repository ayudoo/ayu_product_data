from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProductDetail(models.Model):
    _inherit = ["ayu_product_data.taggable"]
    _name = "ayu_product_data.product_detail"
    _description = "Product Detail"
    _rec_name = "attribute_value"
    _order = "section_name, attribute_name, attribute_value"

    _sql_constraints = [
        (
            "unique_name_value",
            "UNIQUE(attribute_name, attribute_value)",
            "The value already exists with this name",
        ),
    ]

    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )
    section_name = fields.Char(string="Section Name", translate=True)
    attribute_name = fields.Char(required=True, string="Attribute Name", translate=True)
    attribute_value = fields.Char(
        required=True, string="Attribute Value", translate=True
    )

    item_group_ids = fields.Many2many(
        "ayu_product_data.item_group",
        relation="ayu_product_data_item_group_detail_rel",
        column1="product_detail_id",
        column2="item_group_id",
        string="Item Groups",
    )
    product_template_ids = fields.Many2many(
        "product.template",
        relation="ayu_product_data_product_template_detail_rel",
        column1="product_detail_id",
        column2="product_template_id",
        string="Product Templates",
    )
    color_ids = fields.Many2many(
        "ayu_product_data.color",
        relation="ayu_product_data_color_detail_rel",
        column1="product_detail_id",
        column2="color_id",
        string="Colors",
    )
    line_ids = fields.Many2many(
        "ayu_product_data.line",
        relation="ayu_product_data_line_detail_rel",
        column1="product_detail_id",
        column2="line_id",
        string="Lines",
    )
    material_ids = fields.Many2many(
        "ayu_product_data.material",
        relation="ayu_product_data_material_detail_rel",
        column1="product_detail_id",
        column2="material_id",
        string="Materials",
    )

    def _get_product_templates_to_update(self):
        return (
            self.product_template_ids
            | self.item_group_ids.product_template_ids
            | self.color_ids.product_template_ids
            | self.line_ids.product_template_ids
            | self.material_ids.product_template_ids
        )

    @api.depends("section_name", "attribute_name", "attribute_value")
    def _compute_display_name(self):
        for record in self:
            parts = [record.attribute_name, record.attribute_value]
            if record.section_name:
                parts = [record.section_name] + parts
            record.display_name = ":".join(parts)

    @api.model
    def name_create(self, name):
        try:
            attribute_name, attribute_value = name.split(":", 1)
        except ValueError:
            raise UserError("For quick create, please use this format, separated by colon: (<section name>:)<attribute name>:<attribute value>")

        if ":" in attribute_name:
            section_name, attribute_name = attribute_name.rsplit(":", 1)
        else:
            section_name = None

        record = self.create(
            {
                "section_name": section_name,
                "attribute_name": attribute_name,
                "attribute_value": attribute_value,
            }
        )
        return record.id, record.display_name

    def copy(self, default=None):
        default = dict(default or {})
        default.update(attribute_value=_("%s (copy)") % (self.attribute_value or ""))
        return super().copy(default)
