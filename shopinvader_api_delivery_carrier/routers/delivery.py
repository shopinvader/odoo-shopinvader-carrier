# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from typing import Annotated

from fastapi import APIRouter, Depends

from odoo import api, fields

from odoo.addons.base.models.res_partner import Partner as ResPartner
from odoo.addons.extendable_fastapi.schemas import PagedCollection
from odoo.addons.fastapi.dependencies import (
    authenticated_partner,
    authenticated_partner_env,
    paging,
)
from odoo.addons.fastapi.schemas import Paging
from odoo.addons.shopinvader_router_helper import VirtualModel

from ..schemas import Picking

delivery_router = APIRouter(tags=["deliveries"])


class DeliveryHelper(VirtualModel):
    _inherit = "shopinvader.router.helper"
    _name = "shopinvader_api_delivery_carrier.delivery_router.helper"
    _description = "ShopInvader API Delivery Router Helper"
    _model = "stock.picking"

    partner = fields.Many2one("res.partner")

    def _domain(self):
        sales = self.env["sale.order"].search(
            [("typology", "=", "sale"), ("partner_id", "=", self.partner.id)]
        )
        return [
            ("sale_id", "in", sales.ids),
            ("picking_type_id.code", "=", "outgoing"),
        ]


def delivery_helper(
    env: Annotated[api.Environment, Depends(authenticated_partner_env)],
    partner: Annotated[ResPartner, Depends(authenticated_partner)],
):
    return env["shopinvader_api_delivery_carrier.delivery_router.helper"].new(
        {"partner": partner}
    )


@delivery_router.get("/deliveries")
def search(
    paging: Annotated[Paging, Depends(paging)],
    helper: Annotated[DeliveryHelper, Depends(delivery_helper)],
) -> PagedCollection[Picking]:
    """Return all outgoing Deliveries for the authenticated partner."""

    count, pickings = helper.search_with_count(
        [],
        limit=paging.limit,
        offset=paging.offset,
    )
    return PagedCollection[Picking](
        count=count, items=[Picking.from_picking(picking) for picking in pickings]
    )
