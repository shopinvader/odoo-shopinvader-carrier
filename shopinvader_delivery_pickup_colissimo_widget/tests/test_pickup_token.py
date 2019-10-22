# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import requests_mock
from odoo.addons.shopinvader.tests.common import CommonCase


class TokenCase(CommonCase):
    def test_get_token(self):
        account = self.env.ref('delivery_roulier_laposte.keychain_la_poste')
        account.clear_password = "laposte_token"
        with self.work_on_services() as work:
            with requests_mock.mock() as m:
                m.post(
                    "https://ws.colissimo.fr/widget-point-retrait"
                    "/rest/authenticate.rest",
                    json={"token": "laposte_token"},
                )
                service = work.component(usage="delivery_pickups")
                res = service.dispatch("get_colissimo_pickup_token")
                self.assertEqual(res, {"token": "laposte_token"})
