# Copyright 2019-2024 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Shopinvader Pickup Public Edition",
    "summary": "Shopinvader Pickup Public Edition",
    "version": "16.0.1.0.0",
    "category": "e-commerce",
    "website": "https://github.com/shopinvader/odoo-shopinvader-carrier",
    "author": "Akretion, Shopinvader",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["shopinvader_api_delivery_pickup"],
    "data": ["views/delivery_carrier_view.xml"],
    "demo": [],
    "qweb": [],
}
