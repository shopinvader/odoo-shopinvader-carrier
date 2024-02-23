# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.osv.expression import FALSE_DOMAIN

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component


class DeliveryPickupService(Component):
    _inherit = "base.shopinvader.service"
    _name = "shopinvader.delivery.pickup.service"
    _usage = "delivery_pickup"
    _description = """
        This service allows you to retrieve the information of available
        pickup sites.
    """

    # Public services:

    def search(self, **params):
        """
        Returns the list of available pickup sites

        If the target params == current_cart, the list will be limited to the
        pickup sites linked to carriers applying to the current cart.

        If you don't provide a carrier_id, the service will return all the
        pickup sites linked to carriers available for this site.

        If you provide a carrier_id, only the pickup sites linked to the given
        carrier are returned except if the carrier is not available for this
        site.

        """
        dropoff_sites = self._search(**params)
        return {
            "count": len(dropoff_sites),
            "rows": [self._dropoff_site_to_json(ds) for ds in dropoff_sites],
        }

    # Validators

    def _validator_search(self):
        return {
            "target": {
                "type": "string",
                "required": False,
                "allowed": ["current_cart"],
            },
            "carrier_id": {
                "type": "integer",
                "coerce": to_int,
                "required": False,
                "nullable": False,
            },
        }

    def _validator_return_search(self):
        return {
            "count": {"type": "integer", "required": True},
            "rows": {
                "type": "list",
                "required": True,
                "schema": {
                    "type": "dict",
                    "schema": self._pickup_site_schema(),
                },
            },
        }

    def _pickup_site_schema(self):
        return {
            "id": {"type": "integer", "required": True},
            "name": {"type": "string", "required": True},
            "ref": {"type": "string", "nullable": True},
            "street": {"type": "string", "nullable": True},
            "street2": {"type": "string", "nullable": True},
            "zip": {"type": "string", "nullable": True},
            "city": {"type": "string", "nullable": True},
            "phone": {"type": "string", "nullable": True},
            "state": {
                "type": "dict",
                "nullable": True,
                "schema": {
                    "id": {"type": "integer", "required": True},
                    "name": {"type": "string", "required": True},
                },
            },
            "country": {
                "type": "dict",
                "nullable": True,
                "schema": {
                    "id": {"type": "integer", "required": True},
                    "name": {"type": "string", "required": True},
                },
            },
            "carrier": {
                "type": "dict",
                "nullable": True,
                "schema": {
                    "id": {"type": "integer", "required": True},
                    "name": {"type": "string", "required": True},
                },
            },
            "attendances": {
                "type": "list",
                "nullable": True,
                "schema": {
                    "type": "dict",
                    "schema": {
                        "id": {"type": "integer", "nullable": True},
                        "dayofweek": {"type": "string", "nullable": True},
                        "hour_from": {"type": "number", "nullable": True},
                        "hour_to": {"type": "number", "nullable": True},
                    },
                },
            },
        }

    # Services implementation

    def _search(self, **params):
        """
        Search for delively carriers
        :param params: see _validator_search
        :return: a list of delivery.carriers
        """
        domain = self._search_param_to_domain(**params)
        return self.env["dropoff.site"].search(domain)

    def _search_param_to_domain(self, **params):
        # first of all, always restrict dropoff site for available carrier
        available_carriers = self.component(usage="delivery_carrier")._search(
            cart=params.get("target")
        )
        carrier_id = params.get("carrier_id")
        if carrier_id:
            if carrier_id not in available_carriers.ids:
                return FALSE_DOMAIN
            return [("carrier_id", "=", carrier_id)]
        return [("carrier_id", "in", available_carriers.ids)]

    def _dropoff_site_to_json(self, dropoff_site):
        return dropoff_site.jsonify(self._json_parser())[0]

    def _json_parser(self):
        return [
            "id",
            "name",
            "ref",
            "street",
            "street2",
            "zip",
            "city",
            "phone",
            ("state_id:state", ["id", "name"]),
            ("country_id:country", ["id", "name"]),
            ("carrier_id:carrier", ["id", "name"]),
            ("attendance_ids:attendances", self._json_parser_attendances()),
        ]

    def _json_parser_attendances(self):
        return ["id", "hour_from", "hour_to", "dayofweek"]
