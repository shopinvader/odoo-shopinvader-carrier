# Copyright 2024 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _is_visible_in_shopinvader_api(self):
        return super()._is_visible_in_shopinvader_api() and not self.is_delivery

    @api.depends("is_delivery")
    def _compute_visible_in_shopinvader_api(self):
        return super()._compute_visible_in_shopinvader_api()
