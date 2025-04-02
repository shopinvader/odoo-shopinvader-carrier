# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from enum import Enum
from typing import Annotated

from extendable_pydantic import StrictExtendableBaseModel
from pydantic import Field

from odoo import api

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

        if self.state:
            domain.append(("state", "=", self.state.value))
        if self.tracking_reference:
            domain.append(("carrier_tracking_ref", "=", self.tracking_reference))
        if self.carrier_id:
            domain.append(("carrier_id", "=", self.carrier_id))
        if self.sale_id:
            domain.append(("sale_id", "=", self.sale_id))
        return domain

class Picking(StrictExtendableBaseModel):
    delivery_id: int
    name: str
    tracking_reference: str | None = None
    delivery_date: datetime | None = Field(
        None, description="Date done or Scheduled Date"
    )
    carrier: DeliveryCarrier | None = None
    sale_id: int | None = None

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
            tracking_reference=odoo_rec.carrier_tracking_ref or None,
            delivery_date=delivery_date,
            carrier=DeliveryCarrier.from_delivery_carrier(odoo_rec.carrier_id)
            if odoo_rec.carrier_id
            else None,
            sale_id=odoo_rec.sale_id.id or None,
        )
