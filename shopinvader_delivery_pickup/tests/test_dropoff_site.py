# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader_delivery_carrier.tests.common import (
    CommonCarrierCase,
)


class DropOffSiteCase(CommonCarrierCase):
    def setUp(self):
        super(DropOffSiteCase, self).setUp()
        self.final_partner = self.cart.partner_shipping_id
        self.poste_carrier.with_dropoff_site = True
        self._set_carrier(self.poste_carrier)
        self.dropoff_site_foo = self.env["dropoff.site"].create(
            {"ref": "foo", "name": "Foo", "carrier_id": self.poste_carrier.id}
        )
        self.dropoff_site_bar = self.env["dropoff.site"].create(
            {"ref": "bar", "name": "Bar", "carrier_id": self.poste_carrier.id}
        )
        self._set_dropoff_site("foo")

    def _set_dropoff_site(self, code):
        self.res_cart = self.service.dispatch(
            "set_dropoff_site", params={"code": code})['data']
        self.res_address = self.res_cart['shipping']['address']

    def test_setting_dropoff_site(self):
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Foo")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )
        self.assertEqual(self.res_address['is_dropoff_site'], True)
        self.assertEqual(self.res_address['recipient_name'], 'Osiris')

    def test_changing_dropoff_site(self):
        previous_shipping = self.cart.partner_shipping_id
        self._set_dropoff_site("bar")
        self.assertNotEqual(self.cart.partner_shipping_id, previous_shipping)
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "bar")
        self.assertEqual(shipping.name, "Bar")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )
        self.assertEqual(self.res_address['is_dropoff_site'], True)
        self.assertEqual(self.res_address['recipient_name'], 'Osiris')

    def test_change_carrier(self):
        cart = self._set_carrier(self.free_carrier)
        address = cart['shipping']['address']
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)
        self.assertNotIn('is_dropoff_site', address)
        self.assertNotIn('recipient_name', address)

    def test_unset_carrier(self):
        self.service._unset_carrier(self.cart)
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)
