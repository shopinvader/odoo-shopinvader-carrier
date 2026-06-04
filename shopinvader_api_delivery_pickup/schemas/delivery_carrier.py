# Copyright 2024 AKRETION
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader_api_delivery_carrier.schemas import delivery_carrier


class DeliveryCarrierWithPrice(delivery_carrier.DeliveryCarrierWithPrice, extends=True):
    with_dropoff_site: bool | None = None

    @classmethod
    def from_delivery_carrier(cls, odoo_rec, cart=None):
        res = super().from_delivery_carrier(odoo_rec, cart=cart)
        res.with_dropoff_site = odoo_rec.with_dropoff_site or None
        return res


class DeliveryCarrier(delivery_carrier.DeliveryCarrier, extends=True):
    with_dropoff_site: bool | None = None

    @classmethod
    def from_delivery_carrier(cls, odoo_rec):
        res = super().from_delivery_carrier(odoo_rec)
        res.with_dropoff_site = odoo_rec.with_dropoff_site or None
        return res
