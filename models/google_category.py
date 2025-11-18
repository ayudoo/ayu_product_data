import logging
import os
import xlrd
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class GoogleProductCategory(models.Model):
    _inherit = ["ayu_product_data.taggable"]
    _name = "ayu_product_data.google_category"
    _description = "Google Product Category"

    _sql_constraints = [
        ("unique_identifier", "UNIQUE(identifier)", "The identifier already exists"),
        ("unique_name", "UNIQUE(name)", "The name already exists"),
    ]

    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )

    identifier = fields.Char(translate=False, required=True)
    name = fields.Char(translate=True, required=True)

    parent_id = fields.Many2one(
        "ayu_product_data.google_category",
        "Parent Category",
        index=True,
        ondelete="cascade",
    )

    item_group_ids = fields.One2many(
        "ayu_product_data.item_group",
        "ayu_google_category_id",
        string="Item Groups",
    )
    product_template_ids = fields.One2many(
        "product.template",
        "ayu_google_category_id",
        string="Product Templates",
    )

    @api.depends("name", "parent_id")
    def _compute_display_name(self):
        for record in self:
            if record.parent_id:
                record.display_name = f"{record.parent_id.display_name} {record.name}"
            else:
                record.display_name = record.name

    @api.model
    def _init_google_categories(self):
        models_dir = os.path.dirname(__file__)
        taxonomy_path = os.path.join(
            models_dir,
            "..",
            "data",
            "google_category",
            "taxonomy-with-ids.en-US.xls",
        )

        book = xlrd.open_workbook(taxonomy_path)
        sheet = book.sheet_by_index(0)
        _logger.info(
            "Load google product category taxonomy with {} rows".format(sheet.nrows)
        )

        exceptions_logged = 0
        last_parents = []

        def trim_last_parents(name):
            rindex = len(last_parents) - 1

            for last_parent in reversed(last_parents):
                if last_parent.name == name:
                    break
                del last_parents[rindex]
                rindex -= 1

        for rx in range(sheet.nrows):
            try:
                row_values = sheet.row_values(rx)
                row_values = [v for v in row_values if v]

                data = {
                    "identifier": int(row_values[0]),
                    "name": row_values[-1],
                }
                parent_name = None
                if len(row_values) > 2:
                    parent_name = row_values[-2]
                    trim_last_parents(parent_name)
                    if last_parents:
                        data["parent_id"] = last_parents[-1].id

                record = self.search([("identifier", "=", data["identifier"])])

                if record:
                    record.update(data)
                else:
                    record = self.create(data)
                last_parents.append(record)

            except Exception as e:
                if exceptions_logged > 5:
                    _logger.error("Exception {} in row {}".format(str(e), rx))
                else:
                    _logger.exception("Exception in row {}:".format(rx))
                    exceptions_logged += 1

    def copy(self, default=None):
        default = dict(default or {})
        default.update(
            identifier=_("%s (copy)") % (self.identifier or ""),
            name=_("%s (copy)") % (self.name or ""),
        )
        return super().copy(default)
