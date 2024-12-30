# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from typing import Annotated

from fastapi import APIRouter, Depends

from odoo import _, api
from odoo.exceptions import UserError

from odoo.addons.sale.models.sale_order import SaleOrder
from odoo.addons.shopinvader_api_cart.routers.cart import cart_helper
from odoo.addons.shopinvader_api_cart.schemas import CartTransaction
from odoo.addons.shopinvader_router_helper import VirtualModel
from odoo.addons.shopinvader_schema_sale.schemas import Sale

from ..schemas import DeliveryCarrierInput

delivery_carrier_cart_router = APIRouter(tags=["carts"])


class CartHelper(VirtualModel):
    _inherit = "shopinvader_api_cart.cart_router.helper"

    # Set carrier
    @api.model
    def _set_carrier_and_price(self, cart, carrier_id):
        ctx = self.env.context.copy()
        ctx.update({"default_order_id": cart.id, "default_carrier_id": carrier_id})
        wizard = self.env["choose.delivery.carrier"].with_context(**ctx).create({})
        wizard._get_shipment_rate()
        wizard.button_confirm()
        return wizard.delivery_price

    @api.model
    def _set_carrier(self, cart, data):
        """
        Check if the carrier is available and set it on the cart.
        """
        carrier_id = data.carrier_id
        if carrier_id not in cart.shopinvader_available_carrier_ids.ids:
            raise UserError(_("This delivery method is not available for your order"))
        self._set_carrier_and_price(cart, carrier_id)

    # Improve cart synchronization: remove carrier everytime an item is updated
    @api.model
    def _sync_cart(
        self,
        cart: SaleOrder,
        uuid: str,
        transactions: list[CartTransaction],
    ):
        cart = super()._sync_cart(cart, uuid, transactions)
        if transactions:
            cart._remove_delivery_line()
        return cart


@delivery_carrier_cart_router.post("/carrier")
@delivery_carrier_cart_router.post("/{uuid}/carrier")
@delivery_carrier_cart_router.post("/current/carrier")
def set_carrier(
    helper: Annotated[CartHelper, Depends(cart_helper)],
    data: DeliveryCarrierInput,
    uuid: str | None = None,
) -> Sale | None:
    """
    If cart is found, set the carrier on it.
    """
    cart = helper._get_cart(uuid)
    if not cart:
        raise UserError(_("There is no cart"))
    helper._set_carrier(cart, data)
    return Sale.from_sale_order(cart) if cart else None
