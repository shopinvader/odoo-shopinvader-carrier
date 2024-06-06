# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from typing import Annotated

import requests
from fastapi import Depends, Request

from odoo import _, api, models
from odoo.exceptions import Warning as UserError

from odoo.addons.fastapi.dependencies import odoo_env
from odoo.addons.shopinvader_api_delivery_pickup.routers import delivery_pickup_router

from ..schemas import DeliveryColissimoPickupToken

_logger = logging.getLogger(__name__)

LAPOSTE_API_ENDPOINT = "https://ws.colissimo.fr/widget-colissimo/rest/"


@delivery_pickup_router.get("/delivery_pickups/providers/colissimo/token")
def colissimo_token_return(
    request: Request,
    odoo_env: Annotated[api.Environment, Depends(odoo_env)],
) -> DeliveryColissimoPickupToken:
    """
    Returns the token for Laposte Account.

    """
    login, password = odoo_env[
        "shopinvader_api_delivery_pickup_colissimo_widget_router.helper"
    ]._get_laposte_account()
    response = requests.post(
        LAPOSTE_API_ENDPOINT + "authenticate.rest",
        json={"login": login, "password": password},
        timeout=3600,
    )
    if response.status_code == 200:
        return response.json()
    else:
        _logger.error("La poste error %s %s", response.status_code, response.text)
        raise UserError(_("Authentification Error with laposte"))


class ShopinvaderApiDeliveryColissimoRouterHelper(models.AbstractModel):
    _name = "shopinvader_api_delivery_pickup_colissimo_widget_router.helper"
    _description = "ShopInvader API Delivery Pickup Colissimo Router Helper"

    def _get_laposte_account(self):
        login = self.env["ir.config_parameter"].get_param("laposte.user")
        password = self.env["ir.config_parameter"].get_param("laposte.password")
        if not login or not password:
            raise UserError(
                _(
                    "The login or password for your Laposte account "
                    "has not been entered in the system settings"
                )
            )
        return login, password
