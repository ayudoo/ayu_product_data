from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_ayu_image_url(self):
        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        website_id = self.env.context.get("website_id")
        if website_id:
            website = self.env["website"].browse(website_id)
        else:
            website = self.env["website"].search([], limit=1)

        for record in self:
            image = record._get_images()[0]
            record.ayu_image_url = "{}{}".format(
                base_url, website.image_url(image, "image_1024")
            )
            record.ayu_image_url_small = "{}{}".format(
                base_url, website.image_url(image, "image_128")
            )

    ayu_image_url = fields.Char(
        string="Image URL", translate=False, compute=_compute_ayu_image_url
    )

    ayu_image_url_small = fields.Char(
        string="Image URL Small", translate=False, compute=_compute_ayu_image_url
    )

    def _compute_ayu_feed_availability(self):
        availibility_threshold = self.env.context.get("availibility_threshold", 0)

        for record in self:
            if record.virtual_available <= availibility_threshold:
                record.ayu_feed_availability = "out_of_stock"
            else:
                record.ayu_feed_availability = "in_stock"

    ayu_feed_availability = fields.Selection(
        [
            ("in_stock", "in_stock"),
            ("out_of_stock", "out_of_stock"),
        ],
        string="Availibility (for Export)",
        translate=False,
        compute=_compute_ayu_feed_availability,
    )
