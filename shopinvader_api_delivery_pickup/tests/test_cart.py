# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json

from requests import Response

from odoo.tests.common import tagged

from odoo.addons.shopinvader_api_cart.routers import cart_router

from .common import TestShopinvaderDeliveryPickupCommon


@tagged("post_install", "-at_install")
class TestCart(TestShopinvaderDeliveryPickupCommon):
    def _set_pickup(self, pickup_site):
        with self._create_test_client(router=cart_router) as test_client:
            data = {
                "pickup_site_id": pickup_site.id,
            }
            response: Response = test_client.post(
                "/set_pickup", content=json.dumps(data)
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.partner_shipping_id, pickup_site.partner_id)
        return response.json()

    def test_setting_pickup_site(self):
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Foo")
        self.assertEqual(shipping, self.final_partner)
        self.assertEqual(self.final_partner.is_dropoff_site, True)
        self.assertEqual(
            self.cart.final_shipping_partner_id.name, "FastAPI Delivery Carrier Demo"
        )
        self.assertEqual(self.cart.carrier_id, self.poste_carrier)

    def test_changing_pickup_site(self):
        previous_shipping = self.cart.partner_shipping_id
        self._set_pickup(self.pickup_site_bar)
        self.assertNotEqual(self.cart.partner_shipping_id, previous_shipping)
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "bar")
        self.assertEqual(shipping.name, "Bar")
        self.assertEqual(shipping, self.final_partner)
        self.assertEqual(self.final_partner.is_dropoff_site, True)
        self.assertEqual(
            self.cart.final_shipping_partner_id.name, "FastAPI Delivery Carrier Demo"
        )
        self.assertEqual(self.cart.carrier_id, self.free_carrier)

    def test_change_carrier(self):
        self._set_carrier(carrier_id=self.free_carrier.id)
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)
        self.assertEqual(self.final_partner.is_dropoff_site, False)
        self.assertEqual(
            self.cart.final_shipping_partner_id.name, "FastAPI Delivery Carrier Demo"
        )

    def test_unset_carrier(self):
        self._set_carrier(carrier_id=False)
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)
