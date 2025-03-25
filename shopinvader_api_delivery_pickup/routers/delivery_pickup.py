# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from odoo import api, models
from odoo.osv import expression

from odoo.addons.base.models.res_partner import Partner as ResPartner
from odoo.addons.delivery_dropoff_site.models.dropoff_site import DropoffSite
from odoo.addons.fastapi.dependencies import (
    authenticated_partner,
    authenticated_partner_env,
)

from ..schemas import DeliveryPickup as DeliveryPickupSchema, DeliveryPickupSearch
from .cart import delivery_pickup_cart_router

delivery_pickup_router = APIRouter(tags=["delivery_pickups"])


@delivery_pickup_router.get("/delivery_pickups")
def search(
    data: Annotated[DeliveryPickupSearch, Depends()],
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated[ResPartner, Depends(authenticated_partner)],
) -> list[DeliveryPickupSchema]:
    """
    Returns the list of all available pickup sites.

    If you don't provide a carrier_id, the service will return all the
    pickup sites linked to carriers available for this site.

    If you provide a carrier_id, only the pickup sites linked to the given
    carrier are returned except if the carrier is not available for this
    site.
    """
    delivery_pickups = (
        env["shopinvader_api_delivery_pickup.delivery_pickup_router.helper"]
        .new({"partner": partner})
        ._search(data, None)
    )
    return [
        DeliveryPickupSchema.from_delivery_pickup(delivery_pickup)
        for delivery_pickup in delivery_pickups
    ]


@delivery_pickup_cart_router.get("/{uuid}/delivery_pickups")
@delivery_pickup_cart_router.get("/current/delivery_pickups")
def search_current(
    data: Annotated[DeliveryPickupSearch, Depends()],
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated[ResPartner, Depends(authenticated_partner)],
    uuid: str | None = None,
) -> list[DeliveryPickupSchema]:
    """
    Returns the list of available pickup sites.

    The list will be limited to the pickup sites linked to carriers applying
    to the current cart.

    If you don't provide a carrier_id, the service will return all the
    pickup sites linked to carriers available for this site.

    If you provide a carrier_id, only the pickup sites linked to the given
    carrier are returned except if the carrier is not available for this
    site.
    """
    cart = env["sale.order"]._find_open_cart(partner.id, str(uuid) if uuid else None)
    if not cart:
        raise HTTPException(status_code=404)

    delivery_pickups = (
        env["shopinvader_api_delivery_pickup.delivery_pickup_router.helper"]
        .new({"partner": partner})
        ._search(data, cart)
    )
    return [
        DeliveryPickupSchema.from_delivery_pickup(delivery_pickup)
        for delivery_pickup in delivery_pickups
    ]


class ShopinvaderApiDeliveryRouterHelper(models.AbstractModel):
    _name = "shopinvader_api_delivery_pickup.delivery_pickup_router.helper"
    _inherit = "shopinvader_api_delivery_carrier.delivery_carrier_router.helper"
    _description = "ShopInvader API Delivery Pickup Router Helper"

    def _search(self, data, cart=None) -> DropoffSite:
        """
        Search for delivery pickup sites
        :return: a list of dropoff.site
        """
        domain = data.to_odoo_domain(self.env)
        if cart:
            delivery_carriers = self._available_carriers(cart)
        else:
            delivery_carriers = self.env["delivery.carrier"].search([])

        delivery_carriers = delivery_carriers.filtered(
            lambda carrier: carrier.with_dropoff_site
        )
        domain = expression.AND(
            [
                domain,
                [("carrier_id", "in", delivery_carriers.ids)],
            ]
        )
        return self.env["dropoff.site"].search(domain)
