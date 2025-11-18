from odoo import fields, models


class BaseMixin(models.AbstractModel):
    """Mixin to reuse in product template and item group.

    Note, that product detail and highligh are handled separetly to allow customization
    on product template level.
    """

    _name = "ayu_product_data.base_mixin"
    _description = "Product Data Base Mixin"

    ayu_google_category_id = fields.Many2one(
        "ayu_product_data.google_category",
        string="Override Google Product Category",
        index=True,
        help="Google will automatically categorize your product based on title,"
        + " description, pricing, brand and GTIN. In specific cases you may need to "
        + " override it.",
    )

    ayu_line_id = fields.Many2one(
        "ayu_product_data.line",
        string="Line",
        index=True,
        help="A range of similar or similarly themed products with different features"
        + " and prices. Not exported in default setting.",
    )

    ayu_color_id = fields.Many2one(
        "ayu_product_data.color",
        string="Color",
        index=True,
    )

    # male, female, unisex - create by xml data
    ayu_gender_id = fields.Many2one(
        "ayu_product_data.gender",
        string="Gender",
        index=True,
    )

    ayu_age_group_id = fields.Many2one(
        "ayu_product_data.age_group",
        string="Age Group",
        index=True,
    )

    ayu_material_id = fields.Many2one(
        "ayu_product_data.material",
        string="Material",
        index=True,
    )

    ayu_condition_id = fields.Many2one(
        "ayu_product_data.condition",
        string="Condition",
        index=True,
    )

    ayu_description_id = fields.Many2one(
        "ayu_product_data.product_text",
        string="Product Description",
        domain=lambda self: [
            (
                "category_id.id",
                "=",
                self.env.ref("ayu_product_data.product_text_category_description").id,
            ),
        ],
        context={'product_text_description': True},
    )

    ayu_product_text_ids = fields.Many2many(
        "ayu_product_data.product_text",
        string="Other Texts",
        domain=lambda self: [
            (
                "category_id.id",
                "!=",
                self.env.ref("ayu_product_data.product_text_category_description").id,
            ),
        ],
    )

    ayu_product_highlight_ids = fields.Many2many(
        "ayu_product_data.product_highlight",
        relation="ayu_product_data_base_highlight_rel",
        string="Product Highlights",
    )

    # TODO remove this after migration
    ayu_country_of_origin_id = fields.Many2one(
        "res.country",
        string="Obsolete Country of Origin",
    )

    @classmethod
    def _get_base_data_fields(cls):
        return [
            "ayu_google_category_id",
            "ayu_line_id",
            "ayu_color_id",
            "ayu_gender_id",
            "ayu_age_group_id",
            "ayu_material_id",
            "ayu_condition_id",
            "ayu_description_id",
            "ayu_product_text_ids",
            "ayu_product_highlight_ids",
            "categ_id",
            "public_categ_ids",
            "country_of_origin",
        ]
