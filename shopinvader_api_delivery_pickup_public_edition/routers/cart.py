# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from typing import Annotated

from fastapi import Depends

from odoo import _, api, models
from odoo.exceptions import UserError

from odoo.addons.base.models.res_partner import Partner as ResPartner
from odoo.addons.fastapi.dependencies import (
    authenticated_partner,
    authenticated_partner_env,
)
from odoo.addons.shopinvader_api_cart.routers import cart_router
from odoo.addons.shopinvader_schema_sale.schemas import Sale

from ..schemas import PublicDeliveryPickupInput


@cart_router.post("/set_public_delivery_pickup")
@cart_router.post("/{uuid}/set_public_delivery_pickup")
@cart_router.post("/current/set_public_delivery_pickup")
def set_public_delivery_pickup(
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated["ResPartner", Depends(authenticated_partner)],
    data: PublicDeliveryPickupInput,
    uuid: str | None = None,
) -> Sale | None:
    """
    If cart is found, set the given dropoffsite on it.
    """
    cart = env["sale.order"]._find_open_cart(partner.id, uuid)
    if not cart:
        raise UserError(_("There is no cart"))
    dropoff_site = env[
        "shopinvader_api_cart.cart_router.helper"
    ]._add_update_dropoff_site(cart, data)
    env["shopinvader_api_cart.cart_router.helper"]._set_delivery_pickup(
        cart, dropoff_site.id
    )
    return Sale.from_sale_order(cart) if cart else None


class ShopinvaderApiCartRouterHelper(models.AbstractModel):
    _inherit = "shopinvader_api_cart.cart_router.helper"

    @api.model
    def _prepare_dropoff_site_params(self, cart, data):
        if not cart.carrier_id:
            raise UserError(_("You must select a carrier first"))
        elif not cart.carrier_id.allow_dropoff_site_public_edition:
            raise UserError(_("You can not add a dropoff site on this carrier"))
        dropoff_site = {
            "ref": data.code,
            "name": data.name,
            "street": data.street,
            "street2": data.street2,
            "zip": data.zip,
            "city": data.city,
            "phone": data.phone,
        }
        country_code = data.country_code
        state_code = data.state_code

        country = self.env["res.country"].search([("code", "=", country_code)])
        if not country:
            raise UserError(_("Invalid country code %(country_code)s"))
        dropoff_site["country_id"] = country.id

        if state_code:
            state = self.env["res.country.state"].search(
                [("code", "=", state_code), ("country_id", "=", country.id)]
            )
            if not state:
                raise UserError(
                    _("Invalid state code %(state_code)s for country %(country_code)s")
                )
            dropoff_site["state_id"] = state.id

        dropoff_site["carrier_id"] = cart.carrier_id.id
        return dropoff_site

    @api.model
    def _add_update_dropoff_site(self, cart, data):
        vals = self._prepare_dropoff_site_params(cart, data)
        dropoff_site = self.env["dropoff.site"].search(
            [
                ("carrier_id", "=", cart.carrier_id.id),
                ("ref", "=", vals["ref"]),
            ]
        )
        if dropoff_site:
            dropoff_site.write(vals)
        else:
            dropoff_site = self.env["dropoff.site"].create(vals)
        return dropoff_site
