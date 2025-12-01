from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import html2plaintext, html_translate
# from odoo.addons.web_editor.models.ir_qweb_fields import html_to_text


class ProductTextCategory(models.Model):
    _name = "ayu_product_data.product_text_category"
    _description = "Product Text Category"
    _order = "sequence"

    _sql_constraints = [
        ("unique_name", "UNIQUE(name)", "The name already exists"),
    ]

    sequence = fields.Integer("Sequence")
    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )
    show_in_product_page = fields.Boolean(
        string="Show in Product Page",
        default=True,
    )
    name = fields.Char(required=True, string="Name", translate=True)

    def unlink(self):
        description_category = self.env.ref(
            "ayu_product_data.product_text_category_description"
        )

        if description_category:
            for record in self:
                if record.id == description_category.id:
                    raise UserError(_("The description category cannot be deleted"))

        return super().unlink()

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=_("%s (copy)") % (self.name or ""))
        return super().copy(default)


class ProductText(models.Model):
    _inherit = ["ayu_product_data.taggable"]
    _name = "ayu_product_data.product_text"
    _description = "Product Text"
    _rec_name = "identifier"
    _order = "category_id, identifier"

    _sql_constraints = [
        (
            "unique_identifier",
            "UNIQUE(identifier, category_id)",
            "The identifier already exists for this category",
        ),
    ]

    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )
    identifier = fields.Char(translate=False, required=True)
    content = fields.Html(
        "Content",
        required=True,
        translate=html_translate,
        sanitize_overridable=True,
        sanitize_attributes=False,
        sanitize_form=False,
    )

    @api.depends("content")
    def _compute_content_plain_text(self):
        for record in self:
            record.content_plain_text = html2plaintext(record.content)
            # record.content_plain_text = html_to_text(record.content)

    content_plain_text = fields.Char(
        "Content (Plain Text)",
        compute=_compute_content_plain_text,
    )
    category_id = fields.Many2one(
        "ayu_product_data.product_text_category",
        string="Category",
        required=True,
    )

    description_pt_ids = fields.One2many(
        "product.template",
        "ayu_description_id",
        string="Description Product Templates",
    )

    product_template_ids = fields.Many2many(
        "product.template",
        relation="ayu_product_data_product_template_product_text_rel",
        string="Product Templates",
        column1="product_text_id",
        column2="product_template_id",
    )

    def _get_product_templates_to_update(self):
        description = self.env.ref("ayu_product_data.product_text_category_description")
        if self.category_id == description:
            return self.description_pt_ids
        else:
            return self.product_template_ids

    @api.depends("category_id", "identifier", "content")
    def _compute_display_name(self):
        description_category = self.env.ref(
            "ayu_product_data.product_text_category_description"
        )
        for record in self:
            if record.content:
                content = html2plaintext(record.content).replace("\n", " ")
                if record.category_id == description_category:
                    name = record.identifier
                    content = content[:200]
                else:
                    if record.category_id:
                        name = f"{record.category_id.name} {record.identifier}"
                    else:
                        name = record.identifier
                    content = content[:50]
                name = f"{name} {content}"
            elif record.identifier:
                name = record.identifier
            else:
                name = "New"

            record.display_name = name

    def copy(self, default=None):
        default = dict(default or {})
        default.update(identifier=_("%s (copy)") % (self.identifier or ""))
        return super().copy(default)
