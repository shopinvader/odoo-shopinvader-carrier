# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api
from odoo.exceptions import UserError

from odoo.addons.shopinvader_router_helper import VirtualModel


class CartHelper(VirtualModel):
    _inherit = "shopinvader_api_cart.cart_router.helper"

    @api.model
    def _set_delivery_pickup(self, cart, data):
        if data.code.startswith("roulier_"):
            # If the code is a Roulier pickup site, we need to upsert it
            # in the database to get its ID.
            carrier = self.env["delivery.carrier"].browse(data.carrier_id)
            if not carrier:
                raise UserError(self.env._("Carrier not found"))
            carrier._roulier_upsert_pickup_site(data.model_dump())

        return super()._set_delivery_pickup(cart, data)
