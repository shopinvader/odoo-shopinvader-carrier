# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from requests import Response

from odoo.addons.shopinvader_api_delivery_carrier.routers import delivery_carrier_router

from .common import TestShopinvaderDeliveryPickupCommon


class TestDeliveryCarrier(TestShopinvaderDeliveryPickupCommon):
    def test_search_all(self):
        with self._create_test_client(router=delivery_carrier_router) as test_client:
            response: Response = test_client.get("/delivery_carriers")
        self.assertEqual(response.status_code, 200)
        res = response.json()
        expected = [
            {
                "id": self.free_carrier.id,
                "name": self.free_carrier.name,
                "code": self.free_carrier.code or None,
                "description": self.free_carrier.carrier_description or None,
                "with_dropoff_site": None,
            },
            {
                "id": self.poste_carrier.id,
                "name": self.poste_carrier.name,
                "code": self.poste_carrier.code or None,
                "description": self.poste_carrier.carrier_description or None,
                "with_dropoff_site": True,
            },
            {
                "id": self.local_carrier.id,
                "name": self.local_carrier.name,
                "code": self.local_carrier.code or None,
                "description": self.local_carrier.carrier_description or None,
                "with_dropoff_site": None,
            },
            {
                "id": self.pickup_carrier.id,
                "name": self.pickup_carrier.name,
                "code": self.pickup_carrier.code or None,
                "description": self.pickup_carrier.carrier_description or None,
                "with_dropoff_site": True,
            },
        ]
        self.assertEqual(res, expected)
