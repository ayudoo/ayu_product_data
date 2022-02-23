from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = ["product.template", "ayu_product_data.base_mixin"]
    _name = "product.template"

    # data from Odoo standard
    #
    # - default_code:   id
    # - barcode:        gtin
    # - website_url:    link
    # - price:          price

    ayu_item_group_id = fields.Many2one(
        "ayu_product_data.item_group",
        string="Item Group",
        index=True,
        help="Used to group your products, similar to variants.",
    )

    @api.model
    def create(self, values):
        record = super().create(values)
        if record.ayu_item_group_id:
            record.ayu_item_group_id._update_product_templates(product_templates=record)
        record._update_product_tags()
        return record

    def write(self, values):
        old_values = self._get_old_values(values)
        res = super().write(values)
        self._update_product_tags(old_values=old_values)
        return res

    @classmethod
    def _get_tagged_data_fields(cls):
        fields = cls._get_base_data_fields()
        fields.remove("ayu_country_of_origin_id")
        return fields + [
            "ayu_item_group_id",
            "ayu_custom_product_detail_ids",
        ]

    def _get_old_values(self, values):
        return {
            field: getattr(self, field)
            for field in self._get_tagged_data_fields()
            if field in values
        }

    def _update_product_tags(self, field_names=None, old_values=None):
        if field_names is None:
            field_names = self._get_tagged_data_fields()

        for record in self:
            for field_name in field_names:
                old_value, new_value = record._get_old_new_fields(
                    field_name, old_values
                )

                if new_value != old_value and new_value or old_value:
                    # TODO check for related detail_ids, update as well

                    if old_value:
                        for data_record in old_value:
                            if data_record.tag_ids:
                                data_record._update_prod_tag_rel(
                                    data_record.tag_ids.ids, [], record
                                )
                            record._update_details_tags(data_record, remove=True)

                    if new_value:
                        for data_record in new_value:
                            if data_record.tag_ids:
                                data_record._update_prod_tag_rel(
                                    [], data_record.tag_ids.ids, record
                                )
                            record._update_details_tags(data_record)

    def _update_details_tags(self, data_record, remove=False):
        details = data_record.get_product_details()
        if not details:
            return

        for detail in details:
            if detail.tag_ids:
                if remove:
                    detail._update_prod_tag_rel(detail.tag_ids.ids, [], self)
                else:
                    detail._update_prod_tag_rel([], detail.tag_ids.ids, self)

    def _get_old_new_fields(self, field_name, old_values):
        old_value = None
        new_value = getattr(self, field_name)

        if old_values and field_name in old_values:
            old_value = old_values[field_name]
            if old_value and new_value:
                old_value, new_value = self._strip_unchanged(old_value, new_value)

        return old_value, new_value

    def _strip_unchanged(self, old_value, new_value):
        old = old_value.filtered(lambda x: x not in new_value)
        new_value = new_value.filtered(lambda x: x not in old_value)
        return old, new_value

    @api.onchange("ayu_item_group_id")
    def _compute_item_group_base_data(self):
        for record in self:
            if record.ayu_item_group_id:
                ig = record.ayu_item_group_id
                for field_name in self._get_base_data_fields():
                    data_id = getattr(ig, field_name)
                    if data_id:
                        setattr(record, field_name, data_id)
                        setattr(record, "ig_has_{}".format(field_name), True)
                    else:
                        setattr(record, "ig_has_{}".format(field_name), False)
            else:
                for field_name in self._get_base_data_fields():
                    setattr(record, "ig_has_{}".format(field_name), False)

    ig_has_ayu_google_category_id = fields.Boolean(
        compute=_compute_item_group_base_data
    )
    ig_has_ayu_line_id = fields.Boolean(compute=_compute_item_group_base_data)
    ig_has_ayu_color_id = fields.Boolean(compute=_compute_item_group_base_data)
    ig_has_ayu_gender_id = fields.Boolean(compute=_compute_item_group_base_data)
    ig_has_ayu_age_group_id = fields.Boolean(compute=_compute_item_group_base_data)
    ig_has_ayu_material_id = fields.Boolean(compute=_compute_item_group_base_data)
    ig_has_ayu_condition_id = fields.Boolean(compute=_compute_item_group_base_data)
    ig_has_ayu_description_id = fields.Boolean(compute=_compute_item_group_base_data)
    ig_has_ayu_product_text_ids = fields.Boolean(compute=_compute_item_group_base_data)
    ig_has_public_categ_ids = fields.Boolean(compute=_compute_item_group_base_data)
    ig_has_ayu_product_highlight_ids = fields.Boolean(
        compute=_compute_item_group_base_data
    )

    ig_has_ayu_country_of_origin_id = fields.Boolean(
        compute=_compute_item_group_base_data
    )

    # overridden for table relation and columns
    ayu_product_text_ids = fields.Many2many(
        "ayu_product_data.product_text",
        relation="ayu_product_data_product_template_product_text_rel",
        column1="product_template_id",
        column2="product_text_id",
        string="Other Texts",
        domain=lambda self: [
            (
                "category_id.id",
                "!=",
                self.env.ref("ayu_product_data.product_text_category_description").id,
            ),
        ],
    )

    # product detail

    ayu_custom_product_detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        relation="ayu_product_data_product_template_detail_rel",
        column1="product_template_id",
        column2="product_detail_id",
        string="Product Details",
    )

    @api.onchange("ayu_line_id", "ayu_item_group_id", "ayu_color_id", "ayu_material_id")
    def _compute_ayu_product_detail_ids(self):
        for record in self:
            record.ayu_implied_product_detail_ids = (
                record.ayu_line_id.detail_ids
                + record.ayu_item_group_id.detail_ids
                + record.ayu_color_id.detail_ids
                + record.ayu_material_id.detail_ids
            )
            record.ayu_product_detail_ids = (
                record.ayu_implied_product_detail_ids
                + record.ayu_custom_product_detail_ids
            )

    ayu_implied_product_detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        string="Implied Product Details",
        compute=_compute_ayu_product_detail_ids,
    )
    ayu_item_group_detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        string="Item Group Details",
        related="ayu_item_group_id.custom_detail_ids",
        readonly=1,
    )

    ayu_product_detail_ids = fields.Many2many(
        "ayu_product_data.product_detail",
        string="All Product Details",
        compute=_compute_ayu_product_detail_ids,
    )

    def _compute_ayu_product_detail_text_export(self):
        for record in self:
            record.ayu_product_detail_text_export = ",".join(
                record.ayu_product_detail_ids.mapped("display_name")
            )

    ayu_product_detail_text_export = fields.Char(
        string="Product Details Text Export",
        compute=_compute_ayu_product_detail_text_export,
    )

    # product highlight

    ayu_product_highlight_ids = fields.Many2many(
        "ayu_product_data.product_highlight",
        relation="ayu_product_data_product_template_highlight_rel",
        column1="product_template_id",
        column2="product_highlight_id",
        string="Product Highlights",
    )

    def _compute_ayu_product_highlight_text_export(self):
        for record in self:
            record.ayu_product_highlight_text_export = ",".join(
                [
                    '"{}"'.format(h.display_name.replace('"', ""))
                    for h in record.ayu_product_highlight_ids
                ]
            )

    ayu_product_highlight_text_export = fields.Char(
        string="Product Highlights Text Export",
        compute=_compute_ayu_product_highlight_text_export,
    )

    def _compute_ayu_product_type_text_export(self):
        for record in self:
            record.ayu_product_type_text_export = ", ".join(
                record.public_categ_ids.mapped("product_type_name")
            )

    ayu_product_type_text_export = fields.Char(
        string="eCommerce Categories as product_type",
        help="The eCommerce Categories in the Google Merchant Center product_type"
        + " format",
        compute=_compute_ayu_product_type_text_export,
    )

    def _compute_product_data_specification_help_url(self):
        lang = self.env.context.get("lang", False)
        if not lang:
            lang = "en"
        else:
            lang = lang.split("_", 1)[0]

        for record in self:
            record.product_data_specification_help_url = (
                "https://support.google.com/merchants/answer/7052112?hl={}".format(lang)
            )

    product_data_specification_help_url = fields.Char(
        "Product data specification help URL",
        compute=_compute_product_data_specification_help_url,
    )

    # tags

    ayu_tag_rel_ids = fields.One2many(
        "ayu_product_data.prod_tag_rel",
        "product_template_id",
        string="Tag Assignments",
    )

    # related documents

    ayu_prod_doc_rel_ids = fields.One2many(
        "ayu_product_data.prod_doc_rel",
        "product_template_id",
        string="Related Documents",
        copy=True,
    )

    def get_related_documents(self):
        lang = self.env.context.get("lang") or self.env.user.lang

        return self.ayu_prod_doc_rel_ids.filtered(
            lambda d: d.website_active and d.user_document_id.language_id.code == lang
        )
