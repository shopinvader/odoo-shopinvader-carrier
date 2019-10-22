# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE Sa/ (http://www.acsone.eu)
# Cédric Pigeon <cedric.pigeon@acsone.eu>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.addons.shopinvader.controllers import main
from odoo.http import route

_logger = logging.getLogger(__name__)


class InvaderController(main.InvaderController):
    @route(["/shopinvader/delivery_pickups/get_colissimo_pickup_token"],
            methods=["GET"])
    def get_colissimo_pickup_token(self, **params):
        return self._process_method(
            "delivery_pickups", "get_colissimo_pickup_token", params)
