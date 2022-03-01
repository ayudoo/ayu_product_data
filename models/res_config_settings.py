from odoo import _, api, models, fields
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ayu_product_feed_activation = fields.Boolean(
        compute="compute_ayu_product_feed_activation",
        inverse="inverse_ayu_product_feed_activation",
        string="Activate Feed",
        readonly=False,
    )

    ayu_product_feed_interval_number = fields.Integer(
        default=1,
        help="Product Feed Repeat every x.",
        related="ayu_product_feed_ir_cron_id.interval_number",
        readonly=False,
    )
    ayu_product_feed_interval_type = fields.Selection(
        string="Product Feed Interval Unit",
        default="days",
        related="ayu_product_feed_ir_cron_id.interval_type",
        readonly=False,
    )
    ayu_product_feed_nextcall = fields.Datetime(
        string="Product Feed Next Execution Date",
        related="ayu_product_feed_ir_cron_id.nextcall",
        readonly=False,
    )

    ayu_product_feed_ir_cron_id = fields.Many2one(
        "ir.cron",
        compute="compute_ayu_product_feed_ir_cron_id",
        string="Feed Scheduler",
    )

    def set_values(self):
        super().set_values()
        if self.website_id.ayu_product_feed_id:
            feed = self.website_id.ayu_product_feed_id
            if feed.active and not feed.attachment_ids:
                feed._generate_feed_files()
            else:
                feed.attachment_ids.unlink()

    @api.depends("website_id")
    def compute_ayu_product_feed_activation(self):
        self.ayu_product_feed_activation = (
            self.website_id.ayu_product_feed_id
            and self.website_id.ayu_product_feed_id.active
        )

    def _get_default_feed_export(self):
        export = self.env.ref("ayu_product_data.default_feed_export")
        if not export:
            export = self.env["ir.export"].search(
                [("name", "=", "Default Poduct Data Feed Export")], limit=1
            )
        if not export:
            export = self.env["ir.export"].search([], limit=1)
        if not export:
            raise UserError(
                "No export for the product variants found."
                + " Please create one first. If you name it"
                + " 'Default Poduct Data Feed Export' it will be used by default"
            )
        return export

    @api.depends("website_id")
    @api.onchange("ayu_product_feed_activation")
    def inverse_ayu_product_feed_activation(self):
        if self.ayu_product_feed_activation:
            if self.website_id.ayu_product_feed_id:
                if not self.website_id.ayu_product_feed_id.active:
                    self.website_id.ayu_product_feed_id.active = True
            else:
                export = self._get_default_feed_export()
                feed = self.env["ayu_product_data.feed"].create(
                    {
                        "name": "{} {}".format(self.website_id.name, _("Product Feed")),
                        "export_id": export.id,
                    }
                )
                self.website_id.write({"ayu_product_feed_id": feed.id})
                self.website_id.ayu_product_feed_id = feed
        else:
            self.website_id.ayu_product_feed_id.active = False

    @api.onchange("ayu_product_feed_activation")
    def compute_ayu_product_feed_ir_cron_id(self):
        self.ayu_product_feed_ir_cron_id = self.env.ref(
            "ayu_product_data.ir_cron_generate_feed_files"
        )

    def action_open_feed(self):
        return {
            "view_mode": "form",
            "view_id": self.env.ref("ayu_product_data.view_feed_form").id,
            "res_model": "ayu_product_data.feed",
            "type": "ir.actions.act_window",
            "context": {"create": False},
            "res_id": self.website_id.ayu_product_feed_id.id,
        }
