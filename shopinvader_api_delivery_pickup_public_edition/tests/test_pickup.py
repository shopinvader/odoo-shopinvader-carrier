# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json

from requests import Response

from odoo.tests.common import tagged

from odoo.addons.shopinvader_api_cart.routers import cart_router
from odoo.addons.shopinvader_api_delivery_pickup.tests.common import (
    TestShopinvaderDeliveryPickupCommon,
)


@tagged("post_install", "-at_install")
class PickupCase(TestShopinvaderDeliveryPickupCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.final_partner = cls.cart.partner_shipping_id
        cls.poste_carrier.write(
            {
                "with_dropoff_site": True,
                "allow_dropoff_site_public_edition": True,
            }
        )
        cls._set_carrier(cls.poste_carrier)
        cls._set_public_pickup(ref="foo", name="Bar")

    def _set_public_pickup(self, ref, name):
        with self._create_test_client(router=cart_router) as test_client:
            data = {
                "code": ref,
                "name": name,
                "street": "Boulevard Shopinvader",
                "zip": "69004",
                "city": "Lyon",
                "country_code": "FR",
            }
            response: Response = test_client.post(
                "/set_public_delivery_pickup", content=json.dumps(data)
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.partner_shipping_id.name, name)
        return response.json()

    def test_setting_pickup(self):
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Bar")
        self.assertEqual(self.cart.final_shipping_partner_id, self.final_partner)

    def test_updating_pickup(self):
        shipping = self.cart.partner_shipping_id
        self._set_public_pickup(ref="foo", name="Updated")
        self.assertEqual(self.cart.partner_shipping_id, shipping)
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Updated")
        self.assertEqual(self.cart.final_shipping_partner_id, self.final_partner)

    def test_changing_pickup(self):
        previous_shipping = self.cart.partner_shipping_id
        self._set_public_pickup(ref="foo2", name="Bar2")
        self.assertNotEqual(self.cart.partner_shipping_id, previous_shipping)
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo2")
        self.assertEqual(shipping.name, "Bar2")
        self.assertEqual(self.cart.final_shipping_partner_id, self.final_partner)
