# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component
from odoo.exceptions import UserError
from odoo.tools.translate import _


class CartService(Component):
    _inherit = "shopinvader.cart.service"

    # Public services

    def set_delivery_pickup(self, **params):
        """
            This service will apply the given pickup site AND the linked
            carrier to the current cart
        :param params: Dict containing pickup site information
        :return:
        """
        cart = self._get()
        if not cart:
            raise UserError(_("There is not cart"))
        else:
            self._set_delivery_pickup(cart, params["pickup_site_id"])
            return self._to_json(cart)

    # Validator

    def _validator_set_delivery_pickup(self):
        return {"pickup_site_id": {"coerce": to_int}}

    # Services implementation

    def _set_delivery_pickup(self, cart, pickup_site_id):
        pickup_site_obj = self.env["dropoff.site"]
        pickup_site = pickup_site_obj.search([("id", "=", pickup_site_id)])
        if not pickup_site:
            raise UserError(_("Invalid code for pickup site"))
        self._set_carrier(cart, pickup_site.carrier_id.id)
        vals = {"partner_shipping_id": pickup_site.partner_id.id}
        if not cart.final_shipping_partner_id:
            vals["final_shipping_partner_id"] = cart.partner_shipping_id.id
        cart.write(vals)

    def _reset_delivery_pickup(self, cart):
        if cart.final_shipping_partner_id:
            cart.partner_shipping_id = cart.final_shipping_partner_id
            cart.final_shipping_partner_id = None

    def _set_carrier(self, cart, carrier_id):
        self._reset_delivery_pickup(cart)
        return super(CartService, self)._set_carrier(cart, carrier_id)

    def _unset_carrier(self, cart):
        self._reset_delivery_pickup(cart)
        return super(CartService, self)._unset_carrier(cart)
