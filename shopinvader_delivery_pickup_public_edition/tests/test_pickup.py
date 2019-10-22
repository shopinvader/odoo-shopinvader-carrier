# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader_delivery_carrier.tests.common import (
    CommonCarrierCase,
)


class PickupCase(CommonCarrierCase):
    def setUp(self):
        super(PickupCase, self).setUp()
        self.final_partner = self.cart.partner_shipping_id
        self.poste_carrier.write(
            {
                "with_dropoff_site": True,
                "allow_dropoff_site_public_edition": True,
            }
        )
        self._set_carrier(self.poste_carrier)
        self._set_pickup(ref="foo", name="Bar")

    def _set_pickup(self, ref, name):
        self.service.dispatch(
            "set_public_delivery_pickup",
            params={
                "code": ref,
                "name": name,
                "street": u"Boulevard Shopinvader",
                "zip": u"69004",
                "city": u"Lyon",
                "country_code": u"FR",
            },
        )

    def test_setting_pickup(self):
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Bar")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )

    def test_updating_pickup(self):
        shipping = self.cart.partner_shipping_id
        self._set_pickup(ref="foo", name="Updated")
        self.assertEqual(self.cart.partner_shipping_id, shipping)
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Updated")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )

    def test_changing_pickup(self):
        previous_shipping = self.cart.partner_shipping_id
        self._set_pickup(ref="foo2", name="Bar2")
        self.assertNotEqual(self.cart.partner_shipping_id, previous_shipping)
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo2")
        self.assertEqual(shipping.name, "Bar2")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )
