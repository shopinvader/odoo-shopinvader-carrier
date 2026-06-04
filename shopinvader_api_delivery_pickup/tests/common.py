# Copyright 2019 Akretion (http://www.akretion.com).
# Copyright 2019 ACSONE SA/NV
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from contextlib import contextmanager
from unittest.mock import patch

from requests import Response

from odoo.addons.shopinvader_api_delivery_carrier.routers import (
    delivery_carrier_cart_router,
)
from odoo.addons.shopinvader_api_delivery_carrier.tests.common import (
    TestShopinvaderDeliveryCarrierCommon,
)

from ..routers import delivery_pickup_router


class TestShopinvaderDeliveryPickupCommon(TestShopinvaderDeliveryCarrierCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_with_rights.groups_id = [
            (
                6,
                0,
                [
                    cls.env.ref(
                        "shopinvader_api_delivery_pickup.shopinvader_delivery_pickup_user_group"
                    ).id,
                ],
            )
        ]
        cls.pickup_carrier = cls.env.ref("delivery_dropoff_site.delivery_carrier")
        cls.poste_carrier.with_dropoff_site = True
        cls.cart.carrier_id = cls.poste_carrier.id
        cls.pickup_site_foo = cls.env["dropoff.site"].create(
            {
                "ref": "foo",
                "name": "Foo",
                "carrier_id": cls.poste_carrier.id,
                "code": "FOO",
            }
        )
        cls.pickup_site_bar = cls.env["dropoff.site"].create(
            {
                "ref": "bar",
                "name": "Bar",
                "carrier_id": cls.free_carrier.id,
                "code": "BAR",
            }
        )
        cls.cart.partner_shipping_id = cls.pickup_site_foo.partner_id.id
        cls.cart._onchange_partner_shipping_id()
        cls.final_partner = cls.cart.partner_shipping_id

    def _set_carrier(self, carrier_id):
        with self._create_test_client(
            router=delivery_carrier_cart_router
        ) as test_client:
            data = {
                "carrier_id": carrier_id,
            }
            response: Response = test_client.post("/carrier", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.carrier_id.id, carrier_id)
        self.cart.onchange_partner_shipping_id_final()
        return response.json()

    @contextmanager
    def _mock_geocoder(self):
        def mock_geocode(address, **_kwargs):
            return {
                "Rue de la Paix, 69000 Lyon, FR": (45.6626433, 4.5620656),
                "Rue de la Résistance, 75000 Paris, FR": (49.2568916, 2.4776642),
                "Rue de la République, 69100 Villeurbanne, FR": (45.7733573, 4.8868454),
            }.get(address)

        with patch(
            "odoo.addons.base_geolocalize.models.base_geocoder.GeoCoder.geo_find",
            wraps=mock_geocode,
        ):
            yield

    def _delivery_pickup_search(self, **params):
        with self._create_test_client(router=delivery_pickup_router) as test_client:
            response = test_client.get("/delivery_pickups", params=params)

        self.assertEqual(response.status_code, 200, response.text)
        return response.json()
