# Copyright 2019 ACSONE SA/NV
# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from math import sqrt
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from odoo import api, fields

from odoo.addons.base.models.res_partner import Partner as ResPartner
from odoo.addons.delivery_dropoff_site.models.dropoff_site import DropoffSite
from odoo.addons.fastapi.dependencies import (
    authenticated_partner,
    authenticated_partner_env,
)
from odoo.addons.shopinvader_api_cart.routers.cart import CartHelper, cart_helper
from odoo.addons.shopinvader_router_helper import VirtualModel

from ..schemas import DeliveryPickup, DeliveryPickupSearch
from .cart import delivery_pickup_cart_router

delivery_pickup_router = APIRouter(tags=["delivery_pickups"])


class DeliveryPickupHelper(VirtualModel):
    _inherit = "shopinvader_api_delivery_carrier.delivery_carrier_router.helper"
    _name = "shopinvader_api_delivery_pickup.delivery_pickup_router.helper"
    _description = "ShopInvader API Delivery Pickup Router Helper"
    _model = "dropoff.site"

    partner = fields.Many2one("res.partner")

    def _domain(self):
        return [
            ("partner_latitude", "!=", 0),
            ("partner_longitude", "!=", 0),
        ]

    def _search(self, data, cart=None, limit=10) -> DropoffSite:
        """
        Search for delivery pickup sites
        :return: a list of dropoff.site
        """
        if cart:
            delivery_carriers = self._available_carriers(cart)
        else:
            delivery_carriers = (
                self.env["delivery.carrier"].search([])
                if not data.carrier_id
                else self.env["delivery.carrier"].browse(data.carrier_id)
            )

        delivery_carriers = delivery_carriers.filtered(
            lambda carrier: carrier.with_dropoff_site
        )

        dropoff_sites = self.search(
            [
                ("carrier_id", "in", delivery_carriers.ids),
            ]
        )

        if dropoff_sites:
            # TODO: Order by in db
            res = self.env["res.partner"]._geo_localize(
                data.street, data.zip, data.city, "", data.country
            )
            if not res:
                return self.env["dropoff.site"]

            lat, lng = res

            dropoff_sites = (
                dropoff_sites.sudo()
                .sorted(
                    lambda site: sqrt(
                        (site.partner_latitude - lat) ** 2
                        + (site.partner_longitude - lng) ** 2
                    )
                )[:limit]
                .sudo(False)
            )

        return dropoff_sites


def delivery_pickup_helper(
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated[ResPartner, Depends(authenticated_partner)],
):
    return env["shopinvader_api_delivery_pickup.delivery_pickup_router.helper"].new(
        {"partner": partner}
    )


@delivery_pickup_router.get("/delivery_pickups")
def search(
    data: Annotated[DeliveryPickupSearch, Depends()],
    helper: Annotated[DeliveryPickupHelper, Depends(delivery_pickup_helper)],
) -> list[DeliveryPickup]:
    """
    Returns the list of all available pickup sites.

    If you don't provide a carrier_id, the service will return all the
    pickup sites linked to carriers available for this site.

    If you provide a carrier_id, only the pickup sites linked to the given
    carrier are returned except if the carrier is not available for this
    site.
    """
    delivery_pickups = helper._search(data, None)
    return [
        DeliveryPickup.from_delivery_pickup(delivery_pickup)
        for delivery_pickup in delivery_pickups
    ]


@delivery_pickup_cart_router.get("/{uuid}/delivery_pickups")
@delivery_pickup_cart_router.get("/current/delivery_pickups")
def search_current(
    helper: Annotated[DeliveryPickupHelper, Depends(delivery_pickup_helper)],
    cart_helper: Annotated[CartHelper, Depends(cart_helper)],
    data: Annotated[DeliveryPickupSearch, Depends()],
    uuid: str | None = None,
) -> list[DeliveryPickup]:
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
    cart = cart_helper._get_cart(uuid)
    if not cart:
        raise HTTPException(status_code=404)

    delivery_pickups = helper._search(data, cart)
    return [
        DeliveryPickup.from_delivery_pickup(delivery_pickup)
        for delivery_pickup in delivery_pickups
    ]
