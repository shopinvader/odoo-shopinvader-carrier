# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from odoo import api, models

from odoo.addons.base.models.res_partner import Partner as ResPartner
from odoo.addons.fastapi.dependencies import (
    authenticated_partner,
    authenticated_partner_env,
)
from odoo.addons.shopinvader_api_delivery_pickup.routers.delivery_pickup import (
    search as super_search,
    search_current as super_search_current,
)

from ..schemas.delivery_pickup import DeliveryPickup, DeliveryPickupSearch
from .cart import delivery_pickup_cart_router

_logger = logging.getLogger(__name__)
try:
    from roulier import roulier
except ImportError:
    _logger.debug("Cannot `import roulier`.")


delivery_pickup_router = APIRouter(tags=["delivery_pickups"])


@delivery_pickup_router.get("/delivery_pickups")
def search(
    data: Annotated[DeliveryPickupSearch, Depends()],
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated[ResPartner, Depends(authenticated_partner)],
) -> list[DeliveryPickup]:
    return super_search(data, env, partner)


@delivery_pickup_cart_router.get("/{uuid}/delivery_pickups")
@delivery_pickup_cart_router.get("/current/delivery_pickups")
def search_current(
    data: Annotated[DeliveryPickupSearch, Depends()],
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated[ResPartner, Depends(authenticated_partner)],
    uuid: str | None = None,
) -> list[DeliveryPickup]:
    return super_search_current(data, env, partner, uuid)


class ShopinvaderApiDeliveryRouterHelper(models.AbstractModel):
    _inherit = "shopinvader_api_delivery_pickup.delivery_pickup_router.helper"

    def _available_roulier_carriers(self, cart):
        if cart:
            delivery_carriers = self._available_carriers(cart)
        else:
            delivery_carriers = self.env["delivery.carrier"].search([])

        available_carrier_actions = roulier.get_carriers_action_available()

        delivery_carriers = delivery_carriers.filtered(
            lambda carrier: carrier.with_dropoff_site
            and "search_pickup_sites"
            in available_carrier_actions.get(carrier.delivery_type, [])
        )
        return delivery_carriers

    def _search(self, data, cart=None):
        dropoff_sites = super()._search(data, cart)
        if not data.country or not data.zip:
            # If no country or zip is provided, no roulier lookup
            return dropoff_sites

        roulier_carriers = self._available_roulier_carriers(cart)
        if data.carrier_id:
            roulier_carriers = roulier_carriers.filtered(
                lambda carrier: carrier.id == data.carrier_id
            )

        dropoff_sites = [dropoff_site for dropoff_site in dropoff_sites]

        for carrier in roulier_carriers:
            payload = data.model_dump(exclude={"name", "carrier_id"})
            dropoff_sites.extend(carrier._roulier_search_dropoff_sites(payload))

        return dropoff_sites
