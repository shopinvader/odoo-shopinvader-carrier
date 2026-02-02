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
from odoo.addons.sale.models.sale_order import SaleOrder
from odoo.addons.shopinvader_api_cart.routers import cart_router
from odoo.addons.shopinvader_api_cart.schemas import CartTransaction
from odoo.addons.shopinvader_schema_sale.schemas import Sale

from ..schemas import DeliveryPickupInput


@cart_router.post("/set_pickup")
@cart_router.post("/{uuid}/set_pickup")
@cart_router.post("/current/set_pickup")
def set_delivery_pickup(
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated["ResPartner", Depends(authenticated_partner)],
    data: DeliveryPickupInput,
    uuid: str | None = None,
) -> Sale | None:
    """
    If cart is found, set the pickup site on it.
    """
    cart = env["sale.order"]._find_open_cart(partner.id, uuid)
    if not cart:
        raise UserError(_("There is no cart"))
    env["shopinvader_api_cart.cart_router.helper"]._set_delivery_pickup(
        cart, data.pickup_site_id
    )
    return Sale.from_sale_order(cart) if cart else None


class ShopinvaderApiCartRouterHelper(models.AbstractModel):
    _inherit = "shopinvader_api_cart.cart_router.helper"

    # Set delivery pickup
    @api.model
    def _set_delivery_pickup(self, cart, pickup_site_id):
        pickup_site = self.env["dropoff.site"].search([("id", "=", pickup_site_id)])
        if not pickup_site:
            raise UserError(_("Invalid code for pickup site"))
        if pickup_site.carrier_id not in cart.shopinvader_available_carrier_ids:
            raise UserError(_("This delivery method is not available for your order"))
        self._set_carrier_and_price(cart, pickup_site.carrier_id.id)
        vals = {"partner_shipping_id": pickup_site.partner_id.id}
        if not cart.final_shipping_partner_id:
            vals["final_shipping_partner_id"] = cart.partner_shipping_id.id
        cart.sudo().write(vals)

    @api.model
    def _reset_delivery_pickup(self, cart):
        if cart.final_shipping_partner_id:
            cart.partner_shipping_id = cart.final_shipping_partner_id
            cart.final_shipping_partner_id = None

    @api.model
    def _set_carrier(self, cart, data):
        self._reset_delivery_pickup(cart)
        return super()._set_carrier(cart, data)

    @api.model
    def _sync_cart(
        self,
        partner: ResPartner,
        cart: SaleOrder,
        uuid: str,
        transactions: list[CartTransaction],
    ):
        cart = super()._sync_cart(partner, cart, uuid, transactions)
        if transactions:
            self._reset_delivery_pickup(cart)
        return cart
