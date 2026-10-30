# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from requests import Response

from ..routers import dropoff_site_cart_router
from .common import TestShopinvaderDeliveryDropoffSiteCommon


class TestCart(TestShopinvaderDeliveryDropoffSiteCommon):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_with_rights.groups_id = [
            (
                6,
                0,
                [
                    cls.env.ref(
                        "shopinvader_api_security_sale.shopinvader_sale_user_group"
                    ).id,
                ],
            )
        ]

    def _set_dropoff_site(self, dropoff_site):
        with self._create_test_client(router=dropoff_site_cart_router) as test_client:
            data = {
                "carrier_id": dropoff_site.carrier_id.id,
                "code": dropoff_site.code,
            }
            response: Response = test_client.post("/set_dropoff_site", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.partner_shipping_id, dropoff_site.partner_id)
        self.cart.onchange_partner_shipping_id_final()
        return response.json()

    def test_setting_dropoff_site(self):
        self.cart.onchange_partner_shipping_id_final()
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "foo")
        self.assertEqual(shipping.name, "Foo")
        self.assertEqual(shipping, self.final_partner)
        self.assertEqual(self.final_partner.is_dropoff_site, True)
        self.assertEqual(
            self.cart.final_shipping_partner_id.name, "FastAPI Delivery Carrier Demo"
        )
        self.assertEqual(self.cart.carrier_id, self.poste_carrier)

    def test_changing_dropoff_site(self):
        self._set_carrier(carrier_id=self.free_carrier.id)
        previous_shipping = self.cart.partner_shipping_id
        self._set_dropoff_site(self.dropoff_site_bar)
        self.assertNotEqual(self.cart.partner_shipping_id, previous_shipping)
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "bar")
        self.assertEqual(shipping.name, "Bar")
        self.assertEqual(shipping, self.dropoff_site_bar.partner_id)
        self.assertEqual(self.dropoff_site_bar.is_dropoff_site, True)
        self.assertEqual(
            self.cart.final_shipping_partner_id.name, "FastAPI Delivery Carrier Demo"
        )
        self.assertEqual(self.cart.carrier_id, self.free_carrier)

    def test_changing_dropoff_site_2(self):
        self.cart.final_shipping_partner_id = False
        self._set_carrier(carrier_id=self.free_carrier.id)
        previous_shipping = self.cart.partner_shipping_id
        self._set_dropoff_site(self.dropoff_site_bar)
        self.assertNotEqual(self.cart.partner_shipping_id, previous_shipping)
        shipping = self.cart.partner_shipping_id
        self.assertEqual(shipping.ref, "bar")
        self.assertEqual(shipping.name, "Bar")
        self.assertEqual(shipping, self.dropoff_site_bar.partner_id)
        self.assertEqual(self.dropoff_site_bar.is_dropoff_site, True)
        self.assertEqual(
            self.cart.final_shipping_partner_id.name, "FastAPI Delivery Carrier Demo"
        )
        self.assertEqual(self.cart.carrier_id, self.free_carrier)

    def test_change_carrier(self):
        self._set_carrier(carrier_id=self.free_carrier.id)
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)
        self.assertEqual(self.final_partner.is_dropoff_site, True)
        self.assertEqual(
            self.cart.final_shipping_partner_id.name, "FastAPI Delivery Carrier Demo"
        )

    def test_change_carrier_2(self):
        self.cart.final_shipping_partner_id = self.final_partner
        self._set_carrier(carrier_id=self.free_carrier.id)
        self.assertEqual(self.cart.partner_shipping_id, self.final_partner)

    def test_cart_dropoff_sites(self):
        with (
            self._create_test_client(router=dropoff_site_cart_router) as test_client,
            self._mock_geocoder(),
        ):
            response = test_client.get(
                "/current/dropoff_sites",
                params=dict(
                    country="FR",
                    zip="75000",
                    city="Paris",
                    street="Rue de la Résistance",
                ),
            )

        self.assertEqual(response.status_code, 200, response.text)

    def test_cart_set_dropoff_sites_no_site(self):
        with self._create_test_client(
            router=dropoff_site_cart_router,
            raise_server_exceptions=False,
        ) as test_client:
            data = {
                "carrier_id": self.free_carrier.id,
                "code": "INVALID",
            }
            response: Response = test_client.post("/set_dropoff_site", json=data)
            self.assertEqual(response.status_code, 400, response.text)
            self.assertIn("Invalid code for dropoff site", response.text)

    def test_cart_set_dropoff_sites_bad_carrier(self):
        with self._create_test_client(
            router=dropoff_site_cart_router,
            raise_server_exceptions=False,
        ) as test_client:
            data = {
                "carrier_id": self.free_carrier.id,
                "code": self.free_carrier.code,
            }
            response: Response = test_client.post("/set_dropoff_site", json=data)
            self.assertEqual(response.status_code, 400, response.text)
            self.assertIn("Invalid code for dropoff site", response.text)
