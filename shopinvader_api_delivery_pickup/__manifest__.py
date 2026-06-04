# Copyright 2019-2024 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Shopinvader Delivery Pickup",
    "summary": "Allows to deliver sale order to pickup site",
    "version": "18.0.1.0.0",
    "category": "e-commerce",
    "website": "https://github.com/shopinvader/odoo-shopinvader-carrier",
    "author": "Akretion, ACSONE SA/NV, Shopinvader",
    "development_status": "Alpha",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "shopinvader_api_delivery_carrier",
        "delivery_dropoff_site",
    ],
    "data": [
        "security/groups.xml",
        "security/ir_rule+acl_delivery_pickup.xml",
    ],
}
