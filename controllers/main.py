from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import content_disposition, request


class WebsiteSaleProductDataFeed(WebsiteSale):
    @http.route(
        ["/shop/feed/<string:filename>"],
        type="http",
        auth="public",
        website=True,
    )
    def products_feed(self, filename, **kwargs):
        if self._has_products_feed():
            attachment = request.website.ayu_product_feed_id.attachment_ids.filtered(
                lambda x: x.name == filename
            )

            if attachment:
                return request.make_response(
                    attachment.raw,
                    headers=[
                        ("Content-Type", attachment.mimetype),
                        ("Content-Disposition", content_disposition(attachment.name)),
                    ],
                )

        return request.render("website.page_404")

    def _has_products_feed(self):
        return True
