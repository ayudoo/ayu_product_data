from odoo import _, api, fields, models

TRACKING_FIELDS = [
    "tag_ids",
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
    "identifier",
    "name",
    "categ_id",
    "public_categ_ids",
    "country_of_origin",
    "custom_detail_ids",
    "ayu_product_highlight_ids",
]


class ItemGroup(models.Model):
    _inherit = [
        "mail.thread",
        "mail.activity.mixin",
        "ayu_product_data.base_mixin",
        "ayu_product_data.taggable",
    ]
    _name = "ayu_product_data.item_group"
    _description = "Item Group"
    _order = "identifier"

    _sql_constraints = [
        ("unique_identifier", "UNIQUE(identifier)", "The identifier already exists"),
    ]

    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )

    identifier = fields.Char(translate=False, required=True)
    name = fields.Char(translate=True, required=True)

    product_template_ids = fields.One2many(
        "product.template",
        "ayu_item_group_id",
        string="Product Templates",
    )

    categ_id = fields.Many2one(
        'product.category',
        relation="ayu_product_data_item_group_product_categ_rel",
        string='Product Category',
        help=(
            "Assign categories to this item group to replace the products' categories."
        ),
    )

    public_categ_ids = fields.Many2many(
        "product.public.category",
        relation="ayu_product_data_item_group_product_public_category_rel",
        string="eCommerce Category / Product Type",
        help=(
            "Assign categories to this item group to replace the products' categories."
        ),
    )

    country_of_origin = fields.Many2one(
        "res.country",
        string="Country of Origin",
    )

    def write(self, values):
        old_values = {}
        if "custom_detail_ids" in values:
            # mapped to the product template field
            old_values = {"ayu_item_group_detail_ids": self.custom_detail_ids}

        result = super().write(values)
        for record in self:
            record._update_product_templates(old_values=old_values)

        return result

    def _update_product_templates(self, product_templates=None, old_values=None):
        if product_templates is None:
            product_templates = self.product_template_ids

        for product in product_templates:
            for field_name in self._get_base_data_fields():
                data_id = getattr(self, field_name)
                if data_id:
                    setattr(product, field_name, data_id)

            if old_values:
                product._update_product_tags(
                    field_names=["ayu_item_group_detail_ids"],
                    old_values=old_values,
                )

    # product detail

    custom_detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        relation="ayu_product_data_item_group_detail_rel",
        column1="item_group_id",
        column2="product_detail_id",
        string="Product Details",
    )

    @api.onchange("ayu_line_id", "ayu_color_id", "ayu_material_id")
    def _compute_detail_ids(self):
        for record in self:
            record.implied_detail_ids = (
                record.ayu_line_id.detail_ids
                + record.ayu_color_id.detail_ids
                + record.ayu_material_id.detail_ids
            ) or False
            record.detail_ids = record.implied_detail_ids + record.custom_detail_ids

    implied_detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        string="Implied Product Details",
        compute=_compute_detail_ids,
    )

    detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        string="All Product Details",
        compute=_compute_detail_ids,
    )

    def get_product_details(self):
        return self.custom_detail_ids

    # product hightlight

    ayu_product_highlight_ids = fields.Many2many(
        "ayu_product_data.product_highlight",
        relation="ayu_product_data_item_group_product_highlight_rel",
        column1="item_group_id",
        column2="product_highlight_id",
        string="Product Highlights",
    )

    def name_get(self):
        return [(r.id, " ".join([r.identifier, r.name])) for r in self]

    @api.model
    def name_create(self, name):
        if " " in name:
            identifier, name = name.split(" ", 1)
        else:
            identifier = name

        return self.create(
            {
                "identifier": identifier,
                "name": name,
            }
        ).name_get()[0]

    def _name_search(
        self, name, args=None, operator="ilike", limit=100, name_get_uid=None
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

        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)

    def _compute_website_color_pt_ids(self):
        Product = self.env["product.template"]
        domain = self.env["website"].sale_product_domain()
        domain.append(
            ("ayu_color_id", "!=", False),
        )
        for record in self:
            record.website_color_pt_ids = Product.search(
                domain + [("ayu_item_group_id", "=", record.id)],
                order="ayu_color_id",
            )

    website_color_pt_ids = fields.Many2many(
        "product.template",
        string="Website Color Product Templates",
        compute=_compute_website_color_pt_ids,
    )

    def copy(self, default=None):
        default = dict(default or {})
        default.update(identifier=_("%s (copy)") % (self.identifier or ""))
        return super().copy(default)

    def _track_get_fields(self):
        model_fields = TRACKING_FIELDS
        return model_fields and set(self.fields_get(model_fields, attributes=()))
