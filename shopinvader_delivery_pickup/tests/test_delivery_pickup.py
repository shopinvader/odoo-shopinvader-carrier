# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .common import CommondDeliveryPickupCase


class TestDeliveryCarrier(CommondDeliveryPickupCase):
    def _assertExpectedPickupSites(self, search_result, dropoff_sites):
        self.assertIn("count", search_result)
        self.assertEqual(search_result["count"], len(dropoff_sites))
        pickup_ids = [r["id"] for r in search_result["rows"]]
        self.assertSetEqual(set(dropoff_sites.ids), set(pickup_ids))

    def test_01(self):
        """
        Data:
            * a backend with 2 delivery methods (poste, free)
            * 2 dropoff_site defined for delivery la poste
        Test Case:
            * search delivery_pickup without parameters
        Expected result:
            * 2 pickup site found
        :return:
        """
        res = self._delivery_pickup_search()
        self._assertExpectedPickupSites(
            res, self.pickup_site_foo | self.pickup_site_bar
        )

    def test_02(self):
        """
        Data:
            * a backend without delivery method
            * 2 dropoff_site defined for delivery la poste
        Test Case:
            * search delivery_pickup without parameters
        Expected result:
            * No site found
        :return:
        """
        self.backend.write({"carrier_ids": [(5, None, None)]})
        res = self._delivery_pickup_search()
        self._assertExpectedPickupSites(res, self.env["dropoff.site"].browse())

    def test_03(self):
        """
        Data:
            * a backend without delivery method
            * 2 dropoff_site defined for delivery la poste
        Test Case:
            * search delivery_pickup for carrier la poste
        Expected result:
            * No site found
        :return:
        """
        self.backend.write({"carrier_ids": [(5, None, None)]})
        res = self._delivery_pickup_search(carrier_id=self.poste_carrier.id)
        self._assertExpectedPickupSites(res, self.env["dropoff.site"].browse())

    def test_04(self):
        """
        Data:
            * a backend without 2 delivery methods (poste, free)
            * 1 dropoff_site defined for delivery la poste
            * 1 dropoff_site defined for delivery free
        Test Case:
            * search delivery_pickup for carrier la poste
        Expected result:
            * The result must contains the pickup site linked to poste
        :return:
        """
        self.pickup_site_bar.carrier_id = self.free_carrier
        self.pickup_site_foo.carrier_id = self.poste_carrier
        res = self._delivery_pickup_search(carrier_id=self.poste_carrier.id)
        self._assertExpectedPickupSites(res, self.pickup_site_foo)

    def test_05(self):
        """
        Data:
            * a backend without 2 delivery methods (poste, free)
            * 1 dropoff_site defined for delivery la poste
            * 1 dropoff_site defined for delivery la free
        Test Case:
            * search delivery_pickup for target 'current_cart'
        Expected result:
            * The result must contains the 3 pickup sites since the 2 carriers
            are available on the current cart
        :return:
        """
        self.pickup_site_bar.carrier_id = self.free_carrier
        self.pickup_site_foo.carrier_id = self.poste_carrier
        self._set_carrier(self.poste_carrier)
        res = self._delivery_pickup_search(target="current_cart")
        self._assertExpectedPickupSites(
            res, self.pickup_site_foo | self.pickup_site_bar
        )
