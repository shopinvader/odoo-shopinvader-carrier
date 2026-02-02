# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from typing import Annotated

from fastapi import APIRouter, Depends

from odoo import api, models
from odoo.osv import expression

from odoo.addons.base.models.res_partner import Partner as ResPartner
from odoo.addons.delivery_dropoff_site.models.dropoff_site import DropoffSite
from odoo.addons.fastapi.dependencies import (
    authenticated_partner,
    authenticated_partner_env,
)

from ..schemas import DeliveryPickup as DeliveryPickupSchema, DeliveryPickupSearch

delivery_pickup_router = APIRouter(tags=["delivery_pickups"])


@delivery_pickup_router.get("/delivery_pickups")
def search(
    data: Annotated[DeliveryPickupSearch, Depends()],
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated[ResPartner, Depends(authenticated_partner)],
) -> list[DeliveryPickupSchema]:
    """
    Returns the list of all available pickup sites.

    If cart, the list will be limited to the
    pickup sites linked to carriers applying to the current cart.

    If you don't provide a carrier_id, the service will return all the
    pickup sites linked to carriers available for this site.

    If you provide a carrier_id, only the pickup sites linked to the given
    carrier are returned except if the carrier is not available for this
    site.
    """
    delivery_pickups = (
        env["shopinvader_api_delivery_pickup.delivery_pickup_router.helper"]
        .new({"partner": partner})
        ._search(data, cart=None)
    )
    return [
        DeliveryPickupSchema.from_delivery_pickup(delivery_pickup)
        for delivery_pickup in delivery_pickups
    ]


class ShopinvaderApiDeliveryRouterHelper(models.AbstractModel):
    _name = "shopinvader_api_delivery_pickup.delivery_pickup_router.helper"
    _description = "ShopInvader API Delivery Pickup Router Helper"

    def _search(self, data, cart=None) -> DropoffSite:
        """
        Search for delivery pickup sites
        :return: a list of dropoff.site
        """
        cart.ensure_one()
        domain = data.to_odoo_domain()
        if cart:
            domain = expression.AND(
                domain,
                [("carrier_id", "in", cart.shopinvader_available_carrier_ids.ids)],
            )
        return self.env["dropoff.site"].search(domain)
