# Copyright 2025 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Shopinvader API Delivery Pickup Roulier",
    "summary": "Integrate Roulier pickup sites in Shopinvader",
    "version": "16.0.1.0.0",
    "category": "e-commerce",
    "website": "https://github.com/shopinvader/odoo-shopinvader-carrier",
    "author": "Shopinvader, Akretion",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "installable": True,
    "external_dependencies": {"python": ["roulier"]},
    "depends": ["shopinvader_api_delivery_pickup", "delivery_roulier"],
    "data": [],
    "demo": [],
    "qweb": [],
}
