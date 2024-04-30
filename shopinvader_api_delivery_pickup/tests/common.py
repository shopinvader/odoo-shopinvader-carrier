# Copyright 2019 Akretion (http://www.akretion.com).
# Copyright 2019 ACSONE SA/NV
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json

from requests import Response

from odoo.addons.shopinvader_api_cart.routers import cart_router
from odoo.addons.shopinvader_api_delivery_carrier.tests.common import (
    TestShopinvaderDeliveryCarrierCommon,
)


class TestShopinvaderDeliveryPickupCommon(TestShopinvaderDeliveryCarrierCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_with_rights.groups_id = [
            (4, cls.env.ref("sales_team.group_sale_salesman").id)
        ]
        cls.pickup_carrier = cls.env.ref("delivery_dropoff_site.delivery_carrier")
        cls.poste_carrier.with_dropoff_site = True
        cls.cart.carrier_id = cls.poste_carrier.id
        cls.pickup_site_foo = cls.env["dropoff.site"].create(
            {"ref": "foo", "name": "Foo", "carrier_id": cls.poste_carrier.id}
        )
        cls.pickup_site_bar = cls.env["dropoff.site"].create(
            {"ref": "bar", "name": "Bar", "carrier_id": cls.free_carrier.id}
        )
        cls.cart.partner_shipping_id = cls.pickup_site_foo.partner_id.id
        cls.cart.onchange_partner_shipping_id()
        cls.final_partner = cls.cart.partner_shipping_id

    def _set_carrier(self, carrier_id):
        with self._create_test_client(router=cart_router) as test_client:
            data = {
                "carrier_id": carrier_id,
            }
            response: Response = test_client.post(
                "/set_carrier", content=json.dumps(data)
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.cart.carrier_id.id, carrier_id)
        return response.json()
