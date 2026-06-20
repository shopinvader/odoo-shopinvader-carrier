# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from typing import Annotated

from extendable_pydantic import StrictExtendableBaseModel
from pydantic import Field

from odoo import api


class PublicDeliveryPickupInput(StrictExtendableBaseModel):
    code: str
    name: str
    street: str | None = None
    street2: str | None = None
    zip: str
    city: str
    phone: str | None = None
    state_code: str | None = None
    country_code: str


class PublicDeliveryPickupSearch(StrictExtendableBaseModel):
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


class PublicDeliveryPickup(StrictExtendableBaseModel):
    code: str
    name: str
    street: str | None = None
    street2: str | None = None
    zip: str
    city: str
    phone: str | None = None
    state_code: str | None = None
    country_code: str

    @classmethod
    def from_public_delivery_pickup(cls, odoo_rec):
        return cls.model_construct(
            code=odoo_rec.code,
            name=odoo_rec.name,
            street=odoo_rec.street or None,
            street2=odoo_rec.street2 or None,
            zip=odoo_rec.zip,
            city=odoo_rec.city,
            phone=odoo_rec.phone or None,
            state_code=odoo_rec.state_id.code or None,
            country_code=odoo_rec.country_id.code,
        )
