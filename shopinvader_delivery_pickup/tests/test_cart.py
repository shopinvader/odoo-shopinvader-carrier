# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.shopinvader_delivery_carrier.tests.common import (
    CommonCarrierCase,
)


class TestCart(CommonCarrierCase):
    def setUp(self):
        super(TestCart, self).setUp()
        self.final_partner = self.cart.partner_shipping_id
        self.poste_carrier.with_pickup_site = True
        self._set_carrier(self.poste_carrier)
        self.pickup_site_foo = self.env["dropoff.site"].create(
            {"ref": "foo", "name": "Foo", "carrier_id": self.poste_carrier.id}
        )
        self.pickup_site_bar = self.env["dropoff.site"].create(
            {"ref": "bar", "name": "Bar", "carrier_id": self.free_carrier.id}
        )
        self._set_delivery_pickup(self.pickup_site_foo.id)

    def _set_delivery_pickup(self, pickup_site_id):
        self.res_cart = self.service.dispatch(
            "set_delivery_pickup", params={"pickup_site_id": pickup_site_id}
        )["data"]
        self.res_address = self.res_cart["shipping"]["address"]

    def test_setting_pickup_site(self):
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Foo")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )
        self.assertEqual(self.res_address["is_pickup_site"], True)
        self.assertEqual(self.res_address["recipient_name"], "Osiris")
        self.assertEqual(self.cart.carrier_id, self.poste_carrier)

    def test_changing_pickup_site(self):
        previous_shipping = self.cart.partner_shipping_id
        self._set_delivery_pickup(self.pickup_site_bar.id)
        self.assertNotEqual(self.cart.partner_shipping_id, previous_shipping)
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "bar")
        self.assertEqual(shipping.name, "Bar")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )
        self.assertEqual(self.res_address["is_pickup_site"], True)
        self.assertEqual(self.res_address["recipient_name"], "Osiris")
        self.assertEqual(self.cart.carrier_id, self.free_carrier)

    def test_change_carrier(self):
        cart = self._set_carrier(self.free_carrier)
        address = cart["shipping"]["address"]
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)
        self.assertNotIn("is_pickup_site", address)
        self.assertNotIn("recipient_name", address)

    def test_unset_carrier(self):
        self.service._unset_carrier(self.cart)
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)
