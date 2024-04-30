# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from typing import Annotated, Field, List

from extendable_pydantic import StrictExtendableBaseModel

from odoo import api

from ..schemas import ResourceCalendarAttendance


class DeliveryPickupInput(StrictExtendableBaseModel):
    pickup_site_id: int


class DeliveryPickupSearch(StrictExtendableBaseModel):
    name: Annotated[
        str | None,
        Field(
            description="When used, the search look for any delivery pickup where name "
            "contains the given value case insensitively."
        ),
    ] = None
    carrier_id: Annotated[
        int | None,
        Field(
            description="When used, the search look for any delivery pickup where carrier "
            "contains the given value case insensitively."
        ),
    ] = None

    def to_odoo_domain(self, env: api.Environment):
        domain = []
        if self.name:
            domain.append(("name", "ilike", self.name))
        if self.carrier_id:
            domain.append(("carrier_id", "ilike", self.carrier_id.id))
        return domain


class DeliveryPickup(StrictExtendableBaseModel):
    id: int
    name: str
    code: str | None = None
    partner_id: int
    street: str | None = None
    street2: str | None = None
    zip: str | None = None
    city: str | None = None
    phone: str | None = None
    state_id: int | None = None
    country_id: int
    carrier_id: int
    calendar_id: int | None = None
    attendance_ids: List[ResourceCalendarAttendance] | None = None

    @classmethod
    def from_delivery_pickup(cls, odoo_rec):
        return cls.model_construct(
            id=odoo_rec.id,
            name=odoo_rec.name,
            code=odoo_rec.code or None,
            partner_id=odoo_rec.partner_id.id,
            street=odoo_rec.street or None,
            street2=odoo_rec.street2 or None,
            zip=odoo_rec.zip or None,
            city=odoo_rec.city or None,
            phone=odoo_rec.phone or None,
            state_id=odoo_rec.state_id.id or None,
            country_id=odoo_rec.country_id.id,
            carrier_id=odoo_rec.carrier_id.id,
            calendar_id=odoo_rec.calendar_id.id or None,
            attendance_ids=[
                ResourceCalendarAttendance.from_resource_calendar_attendance(attendance)
                for attendance in odoo_rec.attendance_ids
            ]
            or None,
        )
