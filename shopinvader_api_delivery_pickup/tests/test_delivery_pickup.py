# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests.common import tagged

from .common import TestShopinvaderDeliveryPickupCommon


@tagged("post_install", "-at_install")
class TestDeliveryPickup(TestShopinvaderDeliveryPickupCommon):
    def _assertExpectedPickupSites(self, search_result, dropoff_sites):
        self.assertEqual(len(search_result), len(dropoff_sites))
        pickup_ids = [r["id"] for r in search_result]
        self.assertSetEqual(set(dropoff_sites.ids), set(pickup_ids))

    def _delivery_pickup_search(self, domain):
        return self.env["dropoff.site"].search(domain)

    def test_01(self):
        """
        Data:
            * 2 delivery methods (poste, free)
            * 2 dropoff_site defined for delivery la poste
        Test Case:
            * search delivery_pickup without parameters
        Expected result:
            * 2 pickup sites found
        :return:
        """
        domain = [("carrier_id", "in", self.cart.shopinvader_available_carrier_ids.ids)]
        res = self._delivery_pickup_search(domain)
        self._assertExpectedPickupSites(
            res, self.pickup_site_foo | self.pickup_site_bar
        )

    def test_02(self):
        """
        Data:
            * cart without delivery method
            * 2 dropoff_site defined for delivery la poste
        Test Case:
            * search delivery_pickup without parameters
        Expected result:
            * No site found
        :return:
        """
        self._set_carrier(carrier_id=False)
        domain = [("carrier_id", "=", False)]
        res = self._delivery_pickup_search(domain)
        self._assertExpectedPickupSites(res, self.env["dropoff.site"].browse())

    def test_03(self):
        """
        Data:
            * cart without delivery method
            * 2 dropoff_site defined for delivery la poste
        Test Case:
            * search delivery_pickup for carrier la poste
        Expected result:
            * No site found
        :return:
        """
        self._set_carrier(carrier_id=False)
        domain = [("carrier_id", "=", self.poste_carrier.id)]
        res = self._delivery_pickup_search(domain)
        self._assertExpectedPickupSites(res, self.env["dropoff.site"].browse())

    def test_04(self):
        """
        Data:
            * 2 delivery methods (poste, free) with dropoff_site
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
        domain = [("carrier_id", "=", self.poste_carrier.id)]
        res = self._delivery_pickup_search(domain)
        self._assertExpectedPickupSites(res, self.pickup_site_foo)

    def test_05(self):
        """
        Data:
            * 2 delivery methods (poste, free) with dropoff_site
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
        self._set_carrier(carrier_id=self.poste_carrier.id)
        domain = [("carrier_id", "in", self.cart.shopinvader_available_carrier_ids.ids)]
        res = self._delivery_pickup_search(domain)
        self._assertExpectedPickupSites(
            res, self.pickup_site_foo | self.pickup_site_bar
        )
