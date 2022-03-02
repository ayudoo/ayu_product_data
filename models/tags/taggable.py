from odoo import models, fields, api


class TaggableMixin(models.AbstractModel):
    _name = "ayu_product_data.taggable"
    _description = "Taggable Mixin"

    def _get_tag_domain(self):
        try:
            return [
                (
                    "category_id",
                    "=",
                    self._get_tag_category().id,
                )
            ]
        except Exception:
            return []

    def _get_tag_category(self):
        return self.env.ref(
            "ayu_product_data.tag_category_{}".format(self._name.rsplit(".")[1])
        )

    tag_ids = fields.Many2many(
        "ayu_product_data.tag",
        string="Tags",
        domain=_get_tag_domain,
    )

    @api.onchange("tag_ids")
    def _compute_tag_category(self):
        for record in self:
            try:
                record.tag_category_id = self._get_tag_category()
            except Exception:
                record.tag_category_id = False

    tag_category_id = fields.One2many(
        "ayu_product_data.tag_category",
        string="Tag Category",
        compute=_compute_tag_category,
    )

    def get_product_details(self):
        return False

    def write(self, values):
        old_tag_ids = []
        tag_ids = values.get("tag_ids", False)

        if tag_ids:
            old_tag_ids = self.tag_ids.ids

        res = super().write(values)

        if tag_ids:
            new_tag_ids = self.tag_ids.ids

            removed_tag_ids = [t for t in old_tag_ids if t not in new_tag_ids]
            added_tag_ids = [t for t in new_tag_ids if t not in old_tag_ids]

            self._update_prod_tag_rel(removed_tag_ids, added_tag_ids)

        return res

    def _update_prod_tag_rel(self, removed, added, product_template_ids=None):
        if product_template_ids is None:
            product_template_ids = self._get_product_templates_to_update()

        ProductTagRel = self.env["ayu_product_data.prod_tag_rel"]

        for pt in product_template_ids:
            existing_tag_ids = ProductTagRel.search(
                [
                    ("source_data_model", "=", self._table),
                    ("source_data_id", "=", self.id),
                    ("product_template_id", "=", pt.id),
                    ("tag_id", "in", added),
                ]
            ).tag_id.ids
            for tag_id in added:
                if tag_id not in existing_tag_ids:
                    ProductTagRel.create(
                        {
                            "product_template_id": pt.id,
                            "tag_id": tag_id,
                            "source_data_model": self._table,
                            "source_data_id": self.id,
                        }
                    )

            ProductTagRel.search(
                [
                    ("source_data_model", "=", self._table),
                    ("source_data_id", "=", self.id),
                    ("product_template_id", "=", pt.id),
                    ("tag_id", "in", removed),
                ]
            ).unlink()

    def _get_product_templates_to_update(self):
        return self.product_template_ids

    def unlink(self):
        ProductTagRel = self.env["ayu_product_data.prod_tag_rel"]
        ProductTagRel.search(
            [
                ("source_data_model", "=", self._table),
                ("source_data_id", "in", self.ids),
            ]
        ).unlink()
        return super().unlink()
