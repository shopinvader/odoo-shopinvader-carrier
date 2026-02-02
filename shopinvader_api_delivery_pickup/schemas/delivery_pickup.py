# Copyright 2019 ACSONE SA/NV
# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from typing import List

from extendable_pydantic import StrictExtendableBaseModel

from ..schemas import ResourceCalendarAttendance


class DeliveryPickupInput(StrictExtendableBaseModel):
    carrier_id: int
    code: str


class DeliveryPickupSearch(StrictExtendableBaseModel):
    carrier_id: int | None = None
    country: str
    zip: str
    city: str
    street: str


class DeliveryPickup(StrictExtendableBaseModel):
    carrier_id: int
    code: str
    name: str
    street: str | None = None
    street2: str | None = None
    zip: str | None = None
    city: str | None = None
    phone: str | None = None
    state_id: int | None = None
    country_id: int
    calendar_id: int | None = None
    attendance_ids: List[ResourceCalendarAttendance] | None = None
    lat: float | None = None
    lng: float | None = None

    @classmethod
    def from_delivery_pickup(cls, odoo_rec):
        return cls.model_construct(
            carrier_id=odoo_rec.carrier_id.id,
            code=odoo_rec.code,
            name=odoo_rec.name,
            street=odoo_rec.street or None,
            street2=odoo_rec.street2 or None,
            zip=odoo_rec.zip or None,
            city=odoo_rec.city or None,
            phone=odoo_rec.phone or None,
            state_id=odoo_rec.state_id.id or None,
            country_id=odoo_rec.country_id.id,
            calendar_id=odoo_rec.calendar_id.id or None,
            attendance_ids=[
                ResourceCalendarAttendance.from_resource_calendar_attendance(attendance)
                for attendance in odoo_rec.attendance_ids
            ]
            or None,
            lat=odoo_rec.partner_latitude or None,
            lng=odoo_rec.partner_longitude or None,
        )
