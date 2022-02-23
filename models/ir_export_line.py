from odoo import fields, models


class IrExportsLine(models.Model):
    _inherit = ['ir.exports.line']

    ayu_data_export_label = fields.Char(string='Data Export Label')
