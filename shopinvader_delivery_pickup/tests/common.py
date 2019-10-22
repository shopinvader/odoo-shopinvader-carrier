# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# Copyright 2019 ACSONE SA/NV
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.shopinvader_delivery_carrier.tests.common import (
    CommonCarrierCase,
)


class CommondDeliveryPickupCase(CommonCarrierCase):
    def setUp(self):
        super(CommondDeliveryPickupCase, self).setUp()
        self.final_partner = self.cart.partner_shipping_id
        self.poste_carrier.with_dropoff_site = True
        self._set_carrier(self.poste_carrier)
        self.pickup_site_foo = self.env["dropoff.site"].create(
            {"ref": "foo", "name": "Foo", "carrier_id": self.poste_carrier.id}
        )
        self.pickup_site_bar = self.env["dropoff.site"].create(
            {"ref": "bar", "name": "Bar", "carrier_id": self.free_carrier.id}
        )
        self.cart_service = self.service
        self.delivery_pickup_service = self.cart_service.component(
            usage="delivery_pickups"
        )
        self._cart_set_delivery_pickup(self.pickup_site_foo.id)

    def _cart_set_delivery_pickup(self, pickup_site_id):
        self.res_cart = self.cart_service.dispatch(
            "set_delivery_pickup", params={"pickup_site_id": pickup_site_id}
        )["data"]
        self.res_address = self.res_cart["shipping"]["address"]

    def _delivery_pickup_search(self, **params):
        return self.delivery_pickup_service.dispatch("search", params=params)
