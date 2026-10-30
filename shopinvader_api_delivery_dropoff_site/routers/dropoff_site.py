# Copyright 2019 ACSONE SA/NV
# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from math import sqrt
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from odoo import api, fields

from odoo.addons.base.models.res_partner import Partner as ResPartner
from odoo.addons.delivery_dropoff_site.models.dropoff_site import (
    DropoffSite as DropoffSiteModel,
)
from odoo.addons.fastapi.dependencies import (
    authenticated_partner,
    authenticated_partner_env,
)
from odoo.addons.shopinvader_api_cart.routers.cart import CartHelper, cart_helper
from odoo.addons.shopinvader_router_helper import VirtualModel

from ..schemas import DropoffSite, DropoffSiteSearch
from .cart import dropoff_site_cart_router

dropoff_site_router = APIRouter(tags=["dropoff_sites"])


class DropoffSiteHelper(VirtualModel):
    _inherit = "shopinvader_api_delivery_carrier.delivery_carrier_router.helper"
    _name = "shopinvader_api_delivery_dropoff_site.router.helper"
    _description = "Shopinvader API Delivery Dropoff Site Router Helper"
    _model = "dropoff.site"

    partner = fields.Many2one("res.partner")

    def _domain(self):
        return [
            ("partner_latitude", "!=", 0),
            ("partner_longitude", "!=", 0),
        ]

    def _search(self, data, cart=None, limit=10) -> DropoffSiteModel:
        """
        Search for dropoff sites
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


def dropoff_site_helper(
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated[ResPartner, Depends(authenticated_partner)],
):
    return env["shopinvader_api_delivery_dropoff_site.router.helper"].new(
        {"partner": partner}
    )


@dropoff_site_router.get("/dropoff_sites")
def search(
    data: Annotated[DropoffSiteSearch, Depends()],
    helper: Annotated[DropoffSiteHelper, Depends(dropoff_site_helper)],
) -> list[DropoffSite]:
    """
    Returns the list of all available dropoff sites.

    If you don't provide a carrier_id, the service will return all the
    dropoff sites linked to carriers available for this site.

    If you provide a carrier_id, only the dropoff sites linked to the given
    carrier are returned except if the carrier is not available for this
    site.
    """
    dropoff_sites = helper._search(data, None)
    return [
        DropoffSite.from_dropoff_site(dropoff_site) for dropoff_site in dropoff_sites
    ]


@dropoff_site_cart_router.get("/{uuid}/dropoff_sites")
@dropoff_site_cart_router.get("/current/dropoff_sites")
def search_current(
    helper: Annotated[DropoffSiteHelper, Depends(dropoff_site_helper)],
    cart_helper: Annotated[CartHelper, Depends(cart_helper)],
    data: Annotated[DropoffSiteSearch, Depends()],
    uuid: str | None = None,
) -> list[DropoffSite]:
    """
    Returns the list of available dropoff sites.

    The list will be limited to the dropoff sites linked to carriers applying
    to the current cart.

    If you don't provide a carrier_id, the service will return all the
    dropoff sites linked to carriers available for this site.

    If you provide a carrier_id, only the dropoff sites linked to the given
    carrier are returned except if the carrier is not available for this
    site.
    """
    cart = cart_helper._get_cart(uuid)
    if not cart:
        raise HTTPException(status_code=404)

    dropoff_sites = helper._search(data, cart)
    return [
        DropoffSite.from_dropoff_site(dropoff_site) for dropoff_site in dropoff_sites
    ]
