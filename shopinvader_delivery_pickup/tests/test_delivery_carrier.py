# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp.addons.shopinvader_delivery_carrier.tests.common import (
    CommonCarrierCase,
)


class TestDeliveryCarrier(CommonCarrierCase):
    def setUp(self):
        super(CommonCarrierCase, self).setUp()
        self.carrier_service = self.service.component("delivery_carriers")
        self.poste_carrier.with_dropoff_site = True
        self.pickup_site_foo = self.env["dropoff.site"].create(
            {"ref": "foo", "name": "Foo", "carrier_id": self.poste_carrier.id}
        )

    def test_search_all(self):
        res = self.carrier_service.search()
        expected = {
            "count": 2,
            "rows": [
                {
                    "price": 0.0,
                    "description": None,
                    "id": self.free_carrier.id,
                    "name": self.free_carrier.name,
                    "type": None,
                },
                {
                    "price": 0.0,
                    "description": None,
                    "id": self.poste_carrier.id,
                    "name": self.poste_carrier.name,
                    "type": "pickup",
                },
            ],
        }
        self.assertDictEqual(res, expected)
