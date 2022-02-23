from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    ayu_product_feed_id = fields.Many2one(
        "ayu_product_data.feed", string="Product Data Feed"
    )

    @api.model
    def run_generate_feed_files(self):
        done = set()
        for website in self.search([("ayu_product_feed_id", "!=", False)]):
            if (
                website.ayu_product_feed_id
                and website.ayu_product_feed_id.id not in done
            ):
                website.ayu_product_feed_id._generate_feed_files()
                done.add(website.ayu_product_feed_id.id)
