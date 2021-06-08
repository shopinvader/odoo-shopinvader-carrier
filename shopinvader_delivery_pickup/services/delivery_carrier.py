# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=consider-merging-classes-inherited,method-required-super

from openerp.addons.component.core import Component


class DeliveryCarrierService(Component):
    _inherit = "shopinvader.delivery.carrier.service"

    @property
    def allowed_carrier_types(self):
        res = super(DeliveryCarrierService, self).allowed_carrier_types
        res.append("pickup")
        return res

    def _prepare_carrier(self, carrier, no_price=False):
        res = super(DeliveryCarrierService, self)._prepare_carrier(
            carrier, no_price=no_price
        )
        if carrier.with_dropoff_site:
            res["type"] = "pickup"
        return res
