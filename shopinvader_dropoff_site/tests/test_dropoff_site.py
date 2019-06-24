# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader_delivery_carrier.tests.test_carrier import (
    CommonCarrierCase,
)


class DropOffSiteCase(CommonCarrierCase):
    def setUp(self):
        super(DropOffSiteCase, self).setUp()
        self.final_partner = self.cart.partner_shipping_id
        self.poste_carrier.with_dropoff_site = True
        self._set_carrier(self.poste_carrier)
        self._set_dropoff_site(ref="foo", name="Bar")

    def _set_dropoff_site(self, ref, name):
        self.service.dispatch(
            "apply_dropoff_site",
            params={
                "ref": ref,
                "name": name,
                "street": u"Boulevard Shopinvader",
                "zip": u"69004",
                "city": u"Lyon",
                "country_code": u"FR",
            },
        )

    def test_setting_dropoff_site(self):
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Bar")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )

    def test_updating_dropoff_site(self):
        shipping = self.cart.partner_shipping_id
        self._set_dropoff_site(ref="foo", name="Updated")
        self.assertEqual(self.cart.partner_shipping_id, shipping)
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Updated")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )

    def test_changing_dropoff_site(self):
        previous_shipping = self.cart.partner_shipping_id
        self._set_dropoff_site(ref="foo2", name="Bar2")
        self.assertNotEqual(self.cart.partner_shipping_id, previous_shipping)
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo2")
        self.assertEqual(shipping.name, "Bar2")
        self.assertEqual(
            self.cart.final_shipping_partner_id, self.final_partner
        )

    def test_change_carrier(self):
        self._set_carrier(self.free_carrier)
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)

    def test_unset_carrier(self):
        self.service._unset_carrier(self.cart)
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)
