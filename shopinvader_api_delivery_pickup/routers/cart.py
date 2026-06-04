# Copyright 2019 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from typing import Annotated

from fastapi import APIRouter, Depends

from odoo import api
from odoo.exceptions import UserError

from odoo.addons.sale.models.sale_order import SaleOrder
from odoo.addons.shopinvader_api_cart.routers.cart import cart_helper
from odoo.addons.shopinvader_api_cart.schemas import CartTransaction
from odoo.addons.shopinvader_router_helper import VirtualModel
from odoo.addons.shopinvader_schema_sale.schemas import Sale

from ..schemas import DeliveryPickupInput

delivery_pickup_cart_router = APIRouter(tags=["carts"])


class CartHelper(VirtualModel):
    _inherit = "shopinvader_api_cart.cart_router.helper"

    # Set delivery pickup
    @api.model
    def _set_delivery_pickup(self, cart, data):
        pickup_site = (
            self.env["dropoff.site"]
            .sudo()
            .search(
                [("carrier_id", "=", data.carrier_id), ("code", "=", data.code)],
                limit=1,
            )
        )
        if not pickup_site:
            raise UserError(self.env._("Invalid code for pickup site"))
        if pickup_site.carrier_id not in cart.shopinvader_available_carrier_ids:
            raise UserError(
                self.env._("This delivery method is not available for your order")
            )
        self._set_carrier_and_price(cart, pickup_site.carrier_id.id)
        vals = {"partner_shipping_id": pickup_site.partner_id.id}
        if not cart.final_shipping_partner_id:
            vals["final_shipping_partner_id"] = cart.partner_shipping_id.id
        cart.sudo().write(vals)

    @api.model
    def _reset_delivery_pickup(self, cart):
        cart = cart.sudo()
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
        cart: SaleOrder,
        uuid: str,
        transactions: list[CartTransaction],
    ):
        cart = super()._sync_cart(cart, uuid, transactions)
        if transactions:
            self._reset_delivery_pickup(cart)
        return cart


@delivery_pickup_cart_router.post("/set_pickup")
@delivery_pickup_cart_router.post("/{uuid}/set_pickup")
@delivery_pickup_cart_router.post("/current/set_pickup")
def set_delivery_pickup(
    helper: Annotated[CartHelper, Depends(cart_helper)],
    data: DeliveryPickupInput,
    uuid: str | None = None,
) -> Sale | None:
    """
    If cart is found, set the pickup site on it.
    """
    cart = helper._get_cart(uuid)
    if not cart:
        raise UserError(helper.env._("There is no cart"))
    helper._set_delivery_pickup(cart, data)
    return Sale.from_sale_order(cart) if cart else None
