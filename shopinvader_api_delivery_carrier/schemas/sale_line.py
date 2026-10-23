# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.shopinvader_schema_sale.schemas import sale_line


class SaleLine(sale_line.SaleLine, extends=True):
    qty_delivered: int = 0

    @classmethod
    def from_sale_order_line(cls, odoo_rec):
        res = super().from_sale_order_line(odoo_rec)
        res.qty_delivered = odoo_rec.qty_delivered
        return res

    @classmethod
    def _get_sale_line_type(cls, odoo_rec) -> str:
        if odoo_rec.is_delivery:
            return "delivery"
        return super()._get_sale_line_type(odoo_rec)
