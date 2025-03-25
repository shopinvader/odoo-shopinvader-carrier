# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import Annotated

from fastapi import APIRouter, Depends

from odoo import _, api
from odoo.exceptions import UserError

from odoo.addons.base.models.res_partner import Partner as ResPartner
from odoo.addons.fastapi.dependencies import (
    authenticated_partner,
    authenticated_partner_env,
)
from odoo.addons.shopinvader_api_delivery_pickup.routers.cart import (
    set_delivery_pickup as super_set_delivery_pickup,
)
from odoo.addons.shopinvader_schema_sale.schemas import Sale

from ..schemas.delivery_pickup import DeliveryPickupInput

delivery_pickup_cart_router = APIRouter(tags=["carts"])


@delivery_pickup_cart_router.post("/set_pickup")
@delivery_pickup_cart_router.post("/{uuid}/set_pickup")
@delivery_pickup_cart_router.post("/current/set_pickup")
def set_delivery_pickup(
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated["ResPartner", Depends(authenticated_partner)],
    data: DeliveryPickupInput,
    uuid: str | None = None,
) -> Sale | None:
    if data.type == "roulier":
        carrier = env["delivery.carrier"].browse(data.carrier_id)
        if not carrier:
            raise UserError(_("Carrier not found"))
        pickup_site = carrier._roulier_upsert_pickup_site(
            data.model_dump(exclude={"type", "pickup_site_id"})
        )
        data.pickup_site_id = pickup_site.id
    return super_set_delivery_pickup(env, partner, data, uuid)
