from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    ayu_google_category_id = fields.Many2one(
        "ayu_product_data.google_category",
        string="Google Product Category",
        readonly=True,
    )

    ayu_line_id = fields.Many2one(
        "ayu_product_data.line",
        string="Line",
        readonly=True,
    )

    ayu_color_id = fields.Many2one(
        "ayu_product_data.color",
        string="Color",
        readonly=True,
    )

    ayu_gender_id = fields.Many2one(
        "ayu_product_data.gender",
        string="Gender",
        readonly=True,
    )

    ayu_age_group_id = fields.Many2one(
        "ayu_product_data.age_group",
        string="Age Group",
        readonly=True,
    )

    ayu_material_id = fields.Many2one(
        "ayu_product_data.material",
        string="Material",
        readonly=True,
    )

    ayu_condition_id = fields.Many2one(
        "ayu_product_data.condition",
        string="Condition",
        readonly=True,
    )

    ayu_item_group_id = fields.Many2one(
        "ayu_product_data.item_group",
        string="Item Group",
        readonly=True,
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["ayu_google_category_id"] = "t.ayu_google_category_id"
        res["ayu_line_id"] = "t.ayu_line_id"
        res["ayu_color_id"] = "t.ayu_color_id"
        res["ayu_gender_id"] = "t.ayu_gender_id"
        res["ayu_age_group_id"] = "t.ayu_age_group_id"
        res["ayu_material_id"] = "t.ayu_material_id"
        res["ayu_condition_id"] = "t.ayu_condition_id"
        res["ayu_item_group_id"] = "t.ayu_item_group_id"
        return res

    def _group_by_sale(self):
        return super()._group_by_sale() + (
            ", t.ayu_google_category_id"
            + ", t.ayu_line_id"
            + ", t.ayu_color_id"
            + ", t.ayu_gender_id"
            + ", t.ayu_age_group_id"
            + ", t.ayu_material_id"
            + ", t.ayu_condition_id"
            + ", t.ayu_item_group_id"
        )
