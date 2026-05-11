# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from enum import Enum
from typing import Annotated

from extendable_pydantic import StrictExtendableBaseModel
from pydantic import Field

from odoo import api
from odoo.tools.float_utils import json_float_round

from ..schemas import DeliveryCarrier


class PickingState(str, Enum):
    """Enum for picking states."""

    draft = "draft"
    waiting = "waiting"
    confirmed = "confirmed"
    assigned = "assigned"
    done = "done"
    cancel = "cancel"


class PickingSearch(StrictExtendableBaseModel):
    name: Annotated[
        str | None,
        Field(
            description="Name of the picking. If not provided, all names are returned.",
        ),
    ] = None
    state: Annotated[
        PickingState | None,
        Field(
            description="State of the picking. If not provided, all states are returned.",
        ),
    ] = None
    tracking_reference: Annotated[
        str | None,
        Field(
            description="Tracking reference of the picking. If not provided, "
            "all references are returned.",
        ),
    ] = None
    carrier_id: Annotated[
        int | None,
        Field(
            description="ID of the carrier. If not provided, all carriers are returned.",
        ),
    ] = None
    sale_id: Annotated[
        int | None,
        Field(
            description="ID of the sale order. If not provided, all sales are returned.",
        ),
    ] = None

    def to_odoo_domain(self, env: api.Environment):
        domain = []

        if self.name:
            domain.append(("name", "=", self.name))
        if self.state:
            domain.append(("state", "=", self.state.value))
        if self.tracking_reference:
            domain.append(("carrier_tracking_ref", "=", self.tracking_reference))
        if self.carrier_id:
            domain.append(("carrier_id", "=", self.carrier_id))
        if self.sale_id:
            domain.append(("sale_id", "=", self.sale_id))
        return domain


class PickingLine(StrictExtendableBaseModel):
    product_id: int
    product_name: str
    state: str
    qty: float
    qty_done: float

    @classmethod
    def from_picking_line(cls, odoo_rec):
        return cls.model_construct(
            product_id=odoo_rec.product_id.id,
            product_name=odoo_rec.product_id.name,
            state=odoo_rec.state,
            qty=json_float_round(
                odoo_rec.product_uom_qty,
                precision_digits=len(str(odoo_rec.product_uom.rounding).split(".")[1]),
            ),
            qty_done=json_float_round(
                odoo_rec.quantity,
                precision_digits=len(str(odoo_rec.product_uom.rounding).split(".")[1]),
            ),
        )


class Picking(StrictExtendableBaseModel):
    delivery_id: int
    name: str
    state: PickingState
    tracking_reference: str | None = None
    tracking_url: str | None = None
    delivery_date: datetime | None = Field(
        None, description="Date done or Scheduled Date"
    )
    carrier: DeliveryCarrier | None = None
    sale_id: int | None = None

    lines: list[PickingLine]

    @classmethod
    def from_picking(cls, odoo_rec):
        delivery_date = None
        if odoo_rec.date_done:
            delivery_date = odoo_rec.date_done
        elif odoo_rec.scheduled_date:
            delivery_date = odoo_rec.scheduled_date
        return cls.model_construct(
            delivery_id=odoo_rec.id,
            name=odoo_rec.name,
            state=odoo_rec.state,
            tracking_reference=odoo_rec.carrier_tracking_ref or None,
            tracking_url=odoo_rec.carrier_tracking_url or None,
            delivery_date=delivery_date,
            carrier=DeliveryCarrier.from_delivery_carrier(odoo_rec.carrier_id)
            if odoo_rec.carrier_id
            else None,
            sale_id=odoo_rec.sale_id.id or None,
            lines=[PickingLine.from_picking_line(line) for line in odoo_rec.move_ids],
        )
