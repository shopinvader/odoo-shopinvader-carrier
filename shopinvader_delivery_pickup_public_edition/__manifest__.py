# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Shopinvader Pickup Public Edition",
    "summary": "Shopinvader Pickup Public Edition",
    "version": "10.0.0.0.0",
    "category": "e-commerce",
    "website": "https://akretion.com",
    "author": "Akretion",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["shopinvader_delivery_pickup"],
    "data": ["views/delivery_carrier_view.xml"],
    "demo": [],
    "qweb": [],
}
