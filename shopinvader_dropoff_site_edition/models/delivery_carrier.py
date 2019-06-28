# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    allow_dropoff_site_public_edition = fields.Boolean(
        string="Allow Dropoff Site Public Edition",
        help="This option allow to create a dropoff site from public call "
        "on a shopinvader website, this is needed for some carrier",
    )
