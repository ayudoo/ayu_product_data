import io
import logging
from odoo import _, fields, models
from odoo.addons.web.controllers.main import ExportXlsxWriter
from odoo.tools import pycompat

_logger = logging.getLogger(__name__)


def rows_to_csv(fields, rows):
    fp = io.BytesIO()
    writer = pycompat.csv_writer(fp, quoting=1)
    writer.writerow(fields)

    for data in rows:
        row = []
        for d in data:
            if isinstance(d, str) and d.startswith(("=", "-", "+")):
                d = "'" + d

            row.append(pycompat.to_text(d))
        writer.writerow(row)

    return fp.getvalue()


def rows_to_xlsx(fields, rows):
    with ExportXlsxWriter(fields, len(rows)) as xlsx_writer:
        for row_index, row in enumerate(rows):
            for cell_index, cell_value in enumerate(row):
                if isinstance(cell_value, (list, tuple)):
                    cell_value = pycompat.to_text(cell_value)
                xlsx_writer.write_cell(row_index + 1, cell_index, cell_value)

    return xlsx_writer.value


FILE_EXT_DICT = {
    "csv": ("text/csv;charset=utf8", rows_to_csv),
    "xls": ("application/vnd.ms-excel", rows_to_xlsx),
}


class Feed(models.Model):
    _name = "ayu_product_data.feed"
    _description = "Product Data Feed"

    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )

    name = fields.Char(translate=True, required=True)

    context_user_id = fields.Many2one(
        "res.users",
        string="User Context",
        help="The user context for of the product data, for example used for"
        + " pricelist calculations",
        default=lambda self: self.env.ref("base.public_user"),
        required=True,
    )

    country_id = fields.Many2one(
        "res.country", string="User Country", related="context_user_id.country_id",
        readonly=True,
        help="Helper field to quickly see the context country."
    )

    availibility_threshold = fields.Integer(
        'Availibility Threshold',
        help="Forecast quantities lower or equal the threshold are 'out_of_stock'",
        default=0,
    )

    def _compute_website_id(self):
        for record in self:
            record.website_id = self.env["website"].search(
                [("ayu_product_feed_id", "=", record.id)], limit=1
            )

    website_id = fields.Many2one(
        "website", string="Website", compute=_compute_website_id
    )

    def _compute_attachment_ids(self):
        for record in self:
            record.attachment_ids = self.env["ir.attachment"].search(
                [
                    ("res_model", "=", "ayu_product_data.feed"),
                    ("res_id", "=", record.id),
                ]
            )

    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="File",
        ondelete="cascade",
        store=False,
        compute=_compute_attachment_ids,
    )

    def get_default_export_id(self):
        return self.env.ref("ayu_product_data.default_feed_export", None)

    export_id = fields.Many2one(
        "ir.exports",
        string="Export",
        default=get_default_export_id,
        copy=True,
        ondelete="restrict",
        required=True,
    )
    export_fields = fields.One2many(
        "ir.exports.line",
        related="export_id.export_fields",
        string="Export Field",
        readonly=False,
    )

    def open_product_product(self):
        action = {
            "name": _("Products"),
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "target": "current",
            "view_mode": "tree",
        }

        return action

    def action_generate_feed_files(self):
        self._generate_feed_files()

    def _get_feed_products_domain(self):
        return [
            ("sale_ok", "=", True),
            ("website_published", "=", True),
        ]

    def _get_feed_products(self):
        domain = self._get_feed_products_domain()
        pricelist = self.env["product.pricelist"]._get_partner_pricelist_multi(
            self.context_user_id.ids, company_id=self.website_id.company_id.id
        )[self.context_user_id.id]

        Product = (
            self.env["product.product"]
            .with_user(self.context_user_id)
            .with_context(
                availibility_threshold=self.availibility_threshold,
                import_compat=False,
                website_id=self.website_id.id,
                partner=self.context_user_id,
                pricelist=pricelist.id,
            )
            .sudo()
        )

        return Product.search(domain)

    def _generate_feed_filename(self, language, format):
        return "products_{}.{}".format(language.code, format)

    def _generate_feed_files(self):
        if not self.export_id:
            return

        _logger.info("Generating feed files for {} ({})".format(self.name, self.id))

        Attachment = self.env["ir.attachment"]
        products = self._get_feed_products()
        fields = self.export_id.export_fields

        field_names = []
        labels = []
        for field in fields:
            field_names.append(field.name)
            if field.ayu_data_export_label:
                labels.append(field.ayu_data_export_label)
            else:
                labels.append(field.name)

        existing_attachment_ids = self.attachment_ids.ids

        for language in self.website_id.language_ids:
            product_data = (
                products.with_context(lang=language.code)
                .export_data(field_names)
                .get("datas", [])
            )

            for file_extension, info in FILE_EXT_DICT.items():
                mimetype, handler = info

                filename = self._generate_feed_filename(language, file_extension)
                file_data = handler(labels, product_data)

                Attachment.create(
                    {
                        "raw": file_data,
                        "name": filename,
                        "mimetype": mimetype,
                        "res_model": "ayu_product_data.feed",
                        "res_id": self.id,
                    }
                )

        self.env["ir.attachment"].browse(existing_attachment_ids).unlink()
