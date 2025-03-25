# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from pydantic import model_validator

from odoo.addons.delivery_dropoff_site.models.dropoff_site import DropoffSite
from odoo.addons.shopinvader_api_delivery_pickup.schemas import delivery_pickup


class DeliveryPickupInput(delivery_pickup.DeliveryPickupInput, extends=True):
    type: str = "dropoff_site"
    carrier_id: int | None = None
    code: str | None = None
    zone: str | None = None
    pickup_site_id: int | None = None

    @model_validator(mode="after")
    def check_required_fields(self):
        if self.type == "roulier":
            if not self.carrier_id or not self.code or not self.zone:
                raise ValueError("Carrier id zone and code are required")
        elif self.type == "dropoff_site":
            if not self.pickup_site_id:
                raise ValueError("Pickup site id is required")
        return self


class DeliveryPickupSearch(delivery_pickup.DeliveryPickupSearch, extends=True):
    street: str | None = None
    country: str | None = None
    city: str | None = None
    zip: str | None = None


class DeliveryPickup(delivery_pickup.DeliveryPickup, extends=True):
    type: str
    id: int | None = None
    partner_id: int | None = None
    lat: str | None = None
    lng: str | None = None
    zone: str | None = None

    @classmethod
    def from_delivery_pickup(cls, item):
        if isinstance(item, DropoffSite):
            vals = super().from_delivery_pickup(item)
            vals.type = "dropoff_site"
            return vals
        if isinstance(item, dict):
            return cls.model_construct(
                type="roulier",
                name=item["name"],
                code=item["id"],
                street=item["street"],
                zip=item["zip"],
                city=item["city"],
                country_id=item["country_id"],
                lat=item["lat"],
                lng=item["lng"],
                carrier_id=item["carrier_id"],
                zone=item.get("zone"),
            )
        raise TypeError("Expected a DropoffSite or dict, got %s" % type(item))
