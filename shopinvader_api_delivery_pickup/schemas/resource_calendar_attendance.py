# Copyright 2024 AKRETION
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from extendable_pydantic import StrictExtendableBaseModel


class ResourceCalendarAttendance(StrictExtendableBaseModel):
    id: int
    name: str
    hour_from: float
    hour_to: float
    dayofweek: str
    calendar_id: int
    day_period: str

    @classmethod
    def from_resource_calendar_attendance(cls, odoo_rec):
        return cls.model_construct(
            id=odoo_rec.id,
            name=odoo_rec.name,
            hour_from=odoo_rec.hour_from,
            hour_to=odoo_rec.hour_to,
            dayofweek=odoo_rec.dayofweek,
            calendar_id=odoo_rec.calendar_id.id,
            day_period=odoo_rec.day_period,
        )
