# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from roulier import roulier
    from roulier.exception import CarrierError, InvalidApiInput
except ImportError:
    _logger.debug("Cannot `import roulier`.")


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

    def _roulier_search_dropoff_sites(self, search):
        self.ensure_one()
        if not self._is_roulier():
            return []

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
            site["carrier_id"] = self.id
            site["country_id"] = (
                self.env["res.country"].search([("code", "=", site["country"])]).id
            )
        return ret.get("sites", [])

    def _roulier_upsert_pickup_site(self, get):
        self.ensure_one()
        if not self._is_roulier():
            raise UserError(_("Carrier %s is not a Roulier carrier") % self.name)

        get["id"] = get.pop("code", None)
        payload = {
            **self._roulier_get_base_payload(),
            "get": get,
        }
        # api call
        ret = roulier.get(self.delivery_type, "get_pickup_site", payload)

        site = ret.get("site")
        if not site:
            raise UserError(_("Invalid pickup site"))

        vals = {
            "code": site["id"],
            "name": site["name"],
            "street": site["street"],
            "zip": site["zip"],
            "city": site["city"],
            "country_id": self.env["res.country"]
            .search([("code", "=", site["country"])])
            .id,
            "carrier_id": self.id,
        }
        pickup_site = self.env["dropoff.site"].search(
            [("code", "=", get["id"]), ("carrier_id", "=", self.id)], limit=1
        )
        if pickup_site:
            pickup_site.sudo().write(vals)
        else:
            pickup_site = self.env["dropoff.site"].sudo().create(vals)
        pickup_site.flush()
        return pickup_site
