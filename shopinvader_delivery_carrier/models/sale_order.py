# Copyright 2018 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright 2023 Acsone SA/NV.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    shopinvader_available_carrier_ids = fields.Many2many(
        compute="_compute_shopinvader_available_carrier_ids",
        comodel_name="delivery.carrier",
    )

    def _compute_shopinvader_available_carrier_ids(self):
        for order in self:
            order.shopinvader_available_carrier_ids = order._available_carriers()

    def _available_carriers(self):
        self.ensure_one()
        wizard = self.env["choose.delivery.carrier"].new({"order_id": self.id})
        return wizard.available_carrier_ids._origin
