# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

import requests
from odoo import _
from odoo.addons.component.core import Component
from odoo.addons.delivery_roulier_laposte.models.keychain import (
    LAPOSTE_KEYCHAIN_NAMESPACE,
)
from odoo.exceptions import Warning as UserError

_logger = logging.getLogger(__name__)

LAPOSTE_API_ENDPOINT = "https://ws.colissimo.fr/widget-point-retrait/rest/"


class DeliveryPickupService(Component):
    _inherit = "shopinvader.delivery.pickup.service"

    def get_colissimo_pickup_token(self):
        login, password = self._get_laposte_account()
        response = requests.post(
            LAPOSTE_API_ENDPOINT + "authenticate.rest",
            json={"login": login, "password": password},
        )
        if response.status_code == 200:
            return response.json()
        else:
            _logger.error(
                "La poste error %s %s", response.status_code, response.text
            )
            raise UserError(_("Authentification Error with laposte"))

    def _get_laposte_account(self):
        # Note for now we use keychain because the delivery module use it
        # we will remove it later
        account = self.env["keychain.account"]\
            .suspend_security()\
            .retrieve([["namespace", "=", LAPOSTE_KEYCHAIN_NAMESPACE]])
        return account.login, account._get_password()

    # Validator
    def _validator_get_colissimo_pickup_token(self):
        return {}
