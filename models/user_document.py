from odoo import api, fields, models
from odoo.tools import html2plaintext


class RelatedDocument(models.Model):
    _name = "ayu_product_data.prod_doc_rel"
    _description = "Relationship between Products and User Documents"

    _sql_constraints = [
        (
            "unique_rel",
            "UNIQUE(product_template_id,user_document_id)",
            "The product already has this user document",
        ),
    ]

    sequence = fields.Integer("Sequence")

    website_active = fields.Boolean(
        string="Active on Website",
        default=True,
    )

    product_template_id = fields.Many2one(
        comodel_name="product.template",
        ondelete="cascade",
        required=True,
        index=True,
    )

    user_document_id = fields.Many2one(
        comodel_name="ayu_product_data.user_document",
        ondelete="cascade",
        required=True,
        index=True,
    )

    def get_website_download_url(self):
        return (
            "/web/content/?download=true&field=file"
            + "&model=ayu_product_data.user_document"
            + "&filename_field=name"
            + "&id={}".format(self.user_document_id.id)
        )

    # related fields

    active = fields.Boolean(
        string="Active",
        readonly=True,
        related="user_document_id.active",
    )

    name = fields.Char(
        string="Filename",
        readonly=True,
        related="user_document_id.name",
        translate=False,
    )

    language_id = fields.Many2one(
        comodel_name="res.lang",
        string="Language",
        readonly=True,
        related="user_document_id.language_id",
    )

    description = fields.Html(
        string="Description",
        readonly=True,
        related="user_document_id.description",
    )

    description_plain = fields.Char(
        string="Description (Short)",
        related="user_document_id.description_plain",
    )


class UserDocument(models.Model):
    _name = "ayu_product_data.user_document"
    _description = "User Document"
    _order = "name, id"

    active = fields.Boolean(string="Active", default=True)

    name = fields.Char(
        string="Filename",
        required=True,
        translate=False,
    )

    language_id = fields.Many2one(
        comodel_name="res.lang",
        string="Language",
        required=True,
    )

    file = fields.Binary(
        string="File",
        attachment=True,
        required=True,
    )

    description = fields.Html(
        string="Description",
        translate=False,
    )

    @api.depends("description")
    def _compute_description_plain(self):
        for record in self:
            if record.description:
                record.description_plain = html2plaintext(record.description)
            else:
                record.description_plain = ""

    description_plain = fields.Char(
        string="Description (Short)",
        compute=_compute_description_plain,
    )

    prod_doc_rel_ids = fields.One2many(
        "ayu_product_data.prod_doc_rel",
        "user_document_id",
        string="Product Templates",
        readonly=True,
    )
