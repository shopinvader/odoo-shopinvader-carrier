# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from roulier import roulier
    from roulier.exception import CarrierError, InvalidApiInput
except ImportError:
    _logger.debug("Cannot `import roulier`.")
    roulier = None


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    def _roulier_get_base_payload(self):
        fake_picking = self.env["stock.picking"].new({"carrier_id": self})
        account = fake_picking.sudo()._get_account()

        payload = {
            "auth": fake_picking._get_auth(account),
            "service": fake_picking._get_service(account),
        }

        return payload

    def _is_roulier_pickup(self):
        if not roulier:
            return False
        available_carrier_actions = roulier.get_carriers_action_available() or {}
        return "search_pickup_sites" in available_carrier_actions.get(
            self.delivery_type, []
        )

    def _roulier_search_dropoff_sites(self, search):
        self.ensure_one()
        sites = self.env["dropoff.site"]
        if not self._is_roulier_pickup():
            return sites

        payload = {
            **self._roulier_get_base_payload(),
            "search": search,
        }

        try:
            # api call
            ret = roulier.get(self.delivery_type, "search_pickup_sites", payload)
        except InvalidApiInput:
            _logger.warning("InvalidApiInput: %s", exc_info=True)
            return []
        except CarrierError:
            _logger.warning("CarrierError: %s", exc_info=True)
            return []

        for site in ret.get("sites", []):
            code = f"roulier_{site['id']}"
            if site.get("zone"):
                code += f"__{site['zone']}"

            sites |= self.env["dropoff.site"].new(
                {
                    "code": code,
                    "name": site["name"],
                    "street": site["street"],
                    "zip": site["zip"],
                    "city": site["city"],
                    "country_id": self.env["res.country"]
                    .sudo()
                    .search([("code", "=", site["country"])])
                    .id,
                    "carrier_id": self.id,
                    "partner_latitude": site.get("lat"),
                    "partner_longitude": site.get("lng"),
                }
            )

        return sites

    def _roulier_upsert_pickup_site(self, get):
        self.ensure_one()
        if not self._is_roulier():
            raise UserError(
                self.env._("Carrier %s is not a Roulier carrier") % self.name
            )
        code = get["code"]
        if "__" in get["code"]:
            # If the code contains a zone, we need to split it to get the
            # pickup site id.
            get["code"], get["zone"] = get["code"].split("__")

        get["id"] = get["code"].replace("roulier_", "")
        payload = {
            **self._roulier_get_base_payload(),
            "get": get,
        }
        # api call
        ret = roulier.get(self.delivery_type, "get_pickup_site", payload)

        site = ret.get("site")
        if not site:
            raise UserError(self.env._("Invalid pickup site"))

        vals = {
            "code": code,
            "name": site["name"],
            "street": site["street"],
            "zip": site["zip"],
            "city": site["city"],
            "country_id": self.env["res.country"]
            .search([("code", "=", site["country"])])
            .id,
            "carrier_id": self.id,
            "partner_latitude": site.get("lat"),
            "partner_longitude": site.get("lng"),
        }
        pickup_site = self.env["dropoff.site"].search(
            [("code", "=", code), ("carrier_id", "=", self.id)], limit=1
        )
        if pickup_site:
            pickup_site.sudo().write(vals)
        else:
            pickup_site = self.env["dropoff.site"].sudo().create(vals)
        pickup_site.flush()
        return pickup_site
