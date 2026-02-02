# Copyright 2024 AKRETION
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader_schema_address import schemas


class DeliveryAddress(schemas.DeliveryAddress, extends=True):
    is_dropoff_site: bool | None = None

    @classmethod
    def from_res_partner(cls, odoo_rec):
        res = super().from_res_partner(odoo_rec)
        res.is_dropoff_site = odoo_rec.is_dropoff_site or None
        return res
