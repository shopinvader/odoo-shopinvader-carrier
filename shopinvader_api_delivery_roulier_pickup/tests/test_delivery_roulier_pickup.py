# Copyright 2026 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest.mock import MagicMock, patch

from roulier import roulier

from odoo.addons.delivery_roulier.tests.common import (
    DeliveryRoulierCommonCase,
)
from odoo.addons.shopinvader_api_delivery_pickup.tests.common import (
    TestShopinvaderDeliveryPickupCommon,
)

from .common import pickup_sites


class TestDeliveryRoulierPickup(
    TestShopinvaderDeliveryPickupCommon, DeliveryRoulierCommonCase
):
    def setUp(self):
        super().setUp()
        self.pickup_carrier.delivery_type = "test"
        self.carrier_account = self.env["carrier.account"].create(
            {
                "name": "Test Carrier",
                "delivery_type": "test",
                "account": "login",
                "password": "",
            }
        )
        self.pickup_carrier.carrier_account_id = self.carrier_account

    def test_delivery_pickup_roulier(self):
        roulier.get_carriers_action_available = MagicMock(
            return_value={"test": ["search_pickup_sites"]}
        )

        with patch("roulier.roulier.get") as mock_roulier, self._mock_geocoder():
            mock_roulier.return_value = pickup_sites

            res = self._delivery_pickup_search(
                country="FR",
                zip="69000",
                city="Lyon",
                street="Rue de la Paix",
            )

            self.assertEqual(mock_roulier.call_count, 1)
            roulier_args = mock_roulier.mock_calls[0][1]
            self.assertEqual("search_pickup_sites", roulier_args[1])
            roulier_payload = roulier_args[2]

            self.assertEqual(roulier_payload["search"]["country"], "FR")
            self.assertEqual(roulier_payload["search"]["zip"], "69000")
            self.assertEqual(roulier_payload["search"]["city"], "Lyon")
            self.assertEqual(roulier_payload["search"]["street"], "Rue de la Paix")

            self.assertEqual(len(res), 5)
            self.assertEqual(res[0]["name"], "BUREAU DE POSTE LYON SULLY")
            self.assertEqual(res[0]["code"], "roulier_699200__R01")
            self.assertEqual(res[1]["name"], "BUREAU DE POSTE LYON LAFAYETTE")
            self.assertEqual(res[1]["code"], "roulier_693330__R01")
            self.assertEqual(
                res[2]["name"], "BUREAU DE POSTE VILLEURBANNE BELLECOMBE RP"
            )
            self.assertEqual(res[2]["code"], "roulier_060567__R01")
            self.assertEqual(
                res[3]["name"], "BUREAU DE POSTE VILLEURBANNE LES CHARPENNES"
            )
            self.assertEqual(res[3]["code"], "roulier_699370__R01")
            self.assertEqual(res[4]["name"], "BUREAU DE POSTE VILLEURBANNE TOTEM BP")
            self.assertEqual(res[4]["code"], "roulier_699380__R01")
