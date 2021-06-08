# Copyright 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.component.core import AbstractComponent


class AbstractSaleService(AbstractComponent):
    _inherit = "shopinvader.abstract.sale.service"

    def _convert_shipping(self, sale):
        res = super(AbstractSaleService, self)._convert_shipping(sale)
        if sale.partner_shipping_id.is_dropoff_site:
            res["address"].update(
                {
                    "recipient_name": sale.final_shipping_partner_id.name,
                    "is_pickup_site": True,
                }
            )
        return res
