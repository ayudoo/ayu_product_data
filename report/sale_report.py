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

    def _query(self, with_clause="", fields={}, groupby="", from_clause=""):
        fields[
            "ayu_google_category_id"
        ] = ", t.ayu_google_category_id as ayu_google_category_id"
        fields["ayu_line_id"] = ", t.ayu_line_id as ayu_line_id"
        fields["ayu_color_id"] = ", t.ayu_color_id as ayu_color_id"
        fields["ayu_gender_id"] = ", t.ayu_gender_id as ayu_gender_id"
        fields["ayu_age_group_id"] = ", t.ayu_age_group_id as ayu_age_group_id"
        fields["ayu_material_id"] = ", t.ayu_material_id as ayu_material_id"
        fields["ayu_condition_id"] = ", t.ayu_condition_id as ayu_condition_id"
        fields["ayu_item_group_id"] = ", t.ayu_item_group_id as ayu_item_group_id"

        groupby += ", t.ayu_google_category_id"
        groupby += ", t.ayu_line_id"
        groupby += ", t.ayu_color_id"
        groupby += ", t.ayu_gender_id"
        groupby += ", t.ayu_age_group_id"
        groupby += ", t.ayu_material_id"
        groupby += ", t.ayu_condition_id"
        groupby += ", t.ayu_item_group_id"

        return super()._query(with_clause, fields, groupby, from_clause)
