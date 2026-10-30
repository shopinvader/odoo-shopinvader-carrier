# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from .common import TestShopinvaderDeliveryDropoffSiteCommon


class TestDeliveryDropoffSite(TestShopinvaderDeliveryDropoffSiteCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dropoff_site_paris = cls.env["dropoff.site"].create(
            {
                "name": "paris",
                "carrier_id": cls.poste_carrier.id,
                "country_id": cls.env.ref("base.fr").id,
                "city": "Paris",
                "zip": "75000",
                "code": "PARIS",
                "partner_latitude": 48.8575,
                "partner_longitude": 2.3514,
            }
        )
        cls.dropoff_site_lyon = cls.env["dropoff.site"].create(
            {
                "name": "lyon",
                "carrier_id": cls.poste_carrier.id,
                "country_id": cls.env.ref("base.fr").id,
                "city": "Paris",
                "zip": "75000",
                "code": "LYON",
                "partner_latitude": 45.7640,
                "partner_longitude": 4.8357,
            }
        )

    def test_exact(self):
        with self._mock_geocoder():
            res = self._dropoff_site_search(
                country="FR",
                zip="69000",
                city="Lyon",
                street="Rue de la Paix",
            )
        self.assertEqual(
            [ds["code"] for ds in res],
            (self.dropoff_site_lyon | self.dropoff_site_paris).mapped("code"),
        )

    def test_near(self):
        with self._mock_geocoder():
            res = self._dropoff_site_search(
                carrier_id=self.poste_carrier.id,
                country="FR",
                zip="69100",
                city="Villeurbanne",
                street="Rue de la République",
            )
        self.assertEqual(
            [ds["code"] for ds in res],
            (self.dropoff_site_lyon | self.dropoff_site_paris).mapped("code"),
        )

    def test_exact_order(self):
        with self._mock_geocoder():
            res = self._dropoff_site_search(
                country="FR",
                zip="75000",
                city="Paris",
                street="Rue de la Résistance",
            )
        self.assertEqual(
            [ds["code"] for ds in res],
            (self.dropoff_site_paris | self.dropoff_site_lyon).mapped("code"),
        )

    def test_other_carrier(self):
        with self._mock_geocoder():
            res = self._dropoff_site_search(
                carrier_id=self.free_carrier.id,
                country="FR",
                zip="75000",
                city="Paris",
                street="Rue de la Résistance",
            )
        self.assertFalse(res)
