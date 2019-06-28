# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.component.core import Component
from odoo.exceptions import UserError
from odoo.tools.translate import _


class CartService(Component):
    _inherit = "shopinvader.cart.service"

    def set_public_dropoff_site(self, **params):
        """
            This service will create/update apply the given dropoffsite
            to the current cart
        :param params: Dict containing dropoff site information
        :return:
        """
        cart = self._get()
        if not cart:
            raise UserError(_("There is not cart"))
        else:
            self._add_update_dropoff_site(cart, params)
            self._set_dropoff_site(cart, params["code"])
            return self._to_json(cart)

    # Validator
    def _validator_set_public_dropoff_site(self):
        return {
            "code": {"type": "string", "required": True},
            "name": {"type": "string", "required": True},
            "street": {"type": "string"},
            "street2": {"type": "string"},
            "zip": {"type": "string", "required": True},
            "city": {"type": "string", "required": True},
            "phone": {"type": "string"},
            "state_code": {"type": "string"},
            "country_code": {"type": "string", "required": True},
        }

    def _prepare_dropoff_site_params(self, cart, dropoff_site):
        if not cart.carrier_id:
            raise UserError(_("You must select a carrier first"))
        elif not cart.carrier_id.allow_dropoff_site_public_edition:
            raise UserError(
                _("You can not add a dropoff site on this carrier")
            )
        dropoff_site["ref"] = dropoff_site["code"]
        country_code = dropoff_site.pop("country_code")
        state_code = dropoff_site.pop("state_code", None)

        country = self.env["res.country"].search([("code", "=", country_code)])
        if not country:
            raise UserError(_("Invalid country code %s") % country_code)
        dropoff_site["country_id"] = country.id

        if state_code:
            state = self.env["res.country.state"].search(
                [("code", "=", state_code), ("country_id", "=", country.id)]
            )
            if not state:
                raise UserError(
                    _("Invalid state code %s for country %s")
                    % (state_code, country_code)
                )
            dropoff_site["state_id"] = state.id

        dropoff_site["carrier_id"] = cart.carrier_id.id
        return dropoff_site

    def _add_update_dropoff_site(self, cart, dropoff_site):
        vals = self._prepare_dropoff_site_params(cart, dropoff_site)
        dropoff_site_obj = self.env["dropoff.site"]
        dropoff_site = dropoff_site_obj.search(
            [
                ("carrier_id", "=", cart.carrier_id.id),
                ("ref", "=", dropoff_site["ref"]),
            ]
        )
        if dropoff_site:
            dropoff_site.write(vals)
        else:
            dropoff_site = dropoff_site_obj.create(vals)
