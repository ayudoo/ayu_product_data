from collections import defaultdict
from odoo import models, fields, api


class ProductTagRel(models.Model):
    _name = "ayu_product_data.prod_tag_rel"
    _description = "Relationship between Tags and Products"

    _sql_constraints = [
        (
            "unique_rel",
            "UNIQUE(tag_id,product_template_id,source_data_model,source_data_id)",
            "The product already has this tag from this source",
        ),
    ]

    tag_id = fields.Many2one(
        comodel_name="ayu_product_data.tag",
        ondelete="cascade",
        required=True,
        index=True,
    )

    product_template_id = fields.Many2one(
        comodel_name="product.template",
        ondelete="cascade",
        required=True,
        index=True,
    )

    source_data_model = fields.Char("Source Model", readonly=True, index=True)
    source_data_id = fields.Many2oneReference(
        "Source Data ID",
        model_field="source_data_model",
        index=True,
    )

    def _selection_source_data_ref(self):
        return [
            ("ayu_product_data.item_group", "ayu_product_data.item_group"),
            ("ayu_product_data.google_category", "ayu_product_data.google_category"),
            ("ayu_product_data.line", "ayu_product_data.line"),
            ("ayu_product_data.color", "ayu_product_data.color"),
            ("ayu_product_data.gender", "ayu_product_data.gender"),
            ("ayu_product_data.age_group", "ayu_product_data.age_group"),
            ("ayu_product_data.material", "ayu_product_data.material"),
            ("ayu_product_data.condition", "ayu_product_data.condition"),
            ("ayu_product_data.product_text", "ayu_product_data.product_text"),
            ("product.category", "product.category"),
            ("product.public.category", "product.public.category"),
            ("ayu_product_data.product_detail", "ayu_product_data.product_detail"),
            (
                "ayu_product_data.product_highlight",
                "ayu_product_data.product_highlight",
            ),
        ]

    def _compute_source_data_ref(self):
        for record in self:
            if record.source_data_model:
                model_name = record.source_data_model
                if model_name.startswith("ayu_product_data_"):
                    model_name = model_name.replace(
                        "ayu_product_data_", "ayu_product_data."
                    )
                elif model_name == "product_public_category":
                    model_name = "product.public.category"
                elif model_name == "product_category":
                    model_name = "product.category"
                record.source_data_ref = "{},{}".format(
                    model_name, record.source_data_id
                )
            else:
                record.source_data_ref = False

    source_data_ref = fields.Reference(
        string="Source Data Reference",
        selection=_selection_source_data_ref,
        compute=_compute_source_data_ref,
    )


class ProductTag(models.Model):
    _name = "ayu_product_data.tag"
    _description = "Product Tag"
    _order = "sequence,name"

    _sql_constraints = [
        (
            "unique_name",
            "UNIQUE(name,category_id)",
            "The name already exists for this category",
        ),
    ]

    sequence = fields.Integer("Sequence")
    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )
    category_id = fields.Many2one(
        "ayu_product_data.tag_category",
        required=True,
        ondelete="cascade",
    )

    name = fields.Char(translate=True, required=True)
    color = fields.Integer(string="Color Index", default=0)

    use_as_filter = fields.Boolean(
        default=True,
    )
    show_on_detail_page = fields.Boolean(
        default=True,
    )

    product_template_rel_ids = fields.One2many(
        "ayu_product_data.prod_tag_rel",
        "tag_id",
        string="Tag Assignments",
    )

    def name_get(self):
        result = []
        for record in self:
            name = "{} ({})".format(record.name, record.category_id.name)
            result.append((record.id, name))
        return result

    @api.model
    def name_create(self, name):
        category_context = self._context.get("default_category_id", False)
        if category_context:
            category_id = category_context[0][1]
        else:
            category_id = False

        return self.create(
            {
                "name": name,
                "category_id": category_id,
            }
        ).name_get()[0]

    def _get_tag_rel_domain_by_category(self, domain_prefix=""):
        """Returns the domain to filter for
        * any tag in the same category (OR)
        * but tags of all categories (AND)
        """
        mapping = defaultdict(list)
        for tag in self:
            mapping[tag.category_id.id].append(tag.id)
        return [
            ("{}ayu_tag_rel_ids.tag_id".format(domain_prefix), "in", ids)
            for ids in mapping.values()
        ]
