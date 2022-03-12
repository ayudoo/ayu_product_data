from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.osv import expression
from odoo.http import request


class WebsiteSaleProductData(WebsiteSale):

    def _get_search_domain(
        self, search, category, attrib_values, search_in_description=True
    ):
        domain = super()._get_search_domain(
            search, category, attrib_values, search_in_description=search_in_description
        )
        tags = request.context.get("tags", None)
        if tags:
            domain = expression.AND([
                domain, tags._get_tag_rel_domain_by_category()
            ])

        return domain

    def _ayu_get_tags_from_param(self, tag_ids):
        if not tag_ids:
            return []

        if not isinstance(tag_ids, list):
            tag_ids = tag_ids.split("-")

        valid_ids = []
        for tag_id in tag_ids:
            try:
                valid_ids.append(int(tag_id))
            except Exception:
                pass

        return request.env["ayu_product_data.tag"].browse(valid_ids).exists()

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, **post):
        # Unfortunately, Odoo's shop method does not forward the post to search domain.
        # Thus, we do this by the request context
        tag_ids = post.get("tags", None)
        if tag_ids:
            tags = self._ayu_get_tags_from_param(tag_ids)
            ctx = request.context.copy()
            ctx.update(tags=tags)
            request.context = ctx

        res = super().shop(**post)
        return res
