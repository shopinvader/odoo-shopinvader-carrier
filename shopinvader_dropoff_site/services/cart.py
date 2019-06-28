# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.component.core import Component
from odoo.exceptions import UserError
from odoo.tools.translate import _


class CartService(Component):
    _inherit = "shopinvader.cart.service"

    def set_dropoff_site(self, **params):
        """
            This service will apply the given dropoffsite to the current
            cart
        :param params: Dict containing dropoff site information
        :return:
        """
        cart = self._get()
        if not cart:
            raise UserError(_("There is not cart"))
        else:
            self._set_dropoff_site(cart, params["code"])
            return self._to_json(cart)

    # Validator
    def _validator_set_dropoff_site(self):
        return {"code": {"type": "string", "required": True}}

    def _set_dropoff_site(self, cart, dropoff_site_code):
        dropoff_site_obj = self.env["dropoff.site"]
        dropoff_site = dropoff_site_obj.search(
            [
                ("carrier_id", "=", cart.carrier_id.id),
                ("ref", "=", dropoff_site_code),
            ]
        )
        if not dropoff_site:
            raise UserError(_("Invalid code for Dropoff site"))
        vals = {"partner_shipping_id": dropoff_site.partner_id.id}
        if not cart.final_shipping_partner_id:
            vals["final_shipping_partner_id"] = cart.partner_shipping_id.id
        cart.write(vals)

    def _reset_dropoff_site(self, cart):
        if cart.final_shipping_partner_id:
            cart.partner_shipping_id = cart.final_shipping_partner_id
            cart.final_shipping_partner_id = None

    def _set_carrier(self, cart, carrier_id):
        self._reset_dropoff_site(cart)
        return super(CartService, self)._set_carrier(cart, carrier_id)

    def _unset_carrier(self, cart):
        self._reset_dropoff_site(cart)
        return super(CartService, self)._unset_carrier(cart)
