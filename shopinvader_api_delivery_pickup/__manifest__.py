# Copyright 2019 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Shopinvader Delivery Pickup",
    "summary": "Allows to deliver sale order to pickup site",
    "version": "16.0.1.0.0",
    "category": "e-commerce",
    "website": "https://github.com/shopinvader/odoo-shopinvader-carrier",
    "author": "Akretion, ACSONE SA/NV",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["shopinvader_api_delivery_carrier", "delivery_dropoff_site"],
    "data": [],
    "demo": [],
    "qweb": [],
}
