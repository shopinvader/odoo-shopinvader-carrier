# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from math import sqrt

from odoo.addons.shopinvader_router_helper import VirtualModel

_logger = logging.getLogger(__name__)

try:
    from roulier import roulier
except ImportError:
    _logger.debug("Cannot `import roulier`.")


class DeliveryPickupHelper(VirtualModel):
    _inherit = "shopinvader_api_delivery_pickup.delivery_pickup_router.helper"

    def _available_roulier_carriers(self, cart):
        if cart:
            delivery_carriers = self._available_carriers(cart)
        else:
            delivery_carriers = self.env["delivery.carrier"].search([])

        available_carrier_actions = roulier.get_carriers_action_available()

        delivery_carriers = delivery_carriers.filtered(
            lambda carrier: (
                carrier.with_dropoff_site
                and "search_pickup_sites"
                in available_carrier_actions.get(carrier.delivery_type, [])
            )
        )
        return delivery_carriers

    def _search(self, data, cart=None):
        dropoff_sites = super()._search(data, cart)

        roulier_carriers = self._available_roulier_carriers(cart)
        if data.carrier_id:
            roulier_carriers = roulier_carriers.filtered(
                lambda carrier: carrier.id == data.carrier_id
            )

        for carrier in roulier_carriers:
            payload = data.model_dump(exclude={"name", "carrier_id"})
            new_dropoff_sites = carrier._roulier_search_dropoff_sites(payload)
            # Deduplicate saved dropoff sites
            for site in new_dropoff_sites:
                dropoff_sites = dropoff_sites.filtered(
                    lambda site: (
                        not (
                            site.carrier_id == site.carrier_id
                            and site.code == site.code
                        )
                    )
                )
            dropoff_sites |= new_dropoff_sites

        # Sort all dropoff sites by distance to the address
        res = self.env["res.partner"]._geo_localize(
            data.street, data.zip, data.city, "", data.country
        )
        if res:
            lat, lng = res
            dropoff_sites = dropoff_sites.sorted(
                lambda site: sqrt(
                    (site.partner_latitude - lat) ** 2
                    + (site.partner_longitude - lng) ** 2
                )
            )
        return dropoff_sites
