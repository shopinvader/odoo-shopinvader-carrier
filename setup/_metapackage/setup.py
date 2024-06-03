import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-shopinvader-odoo-shopinvader-carrier",
    description="Meta package for shopinvader-odoo-shopinvader-carrier Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-shopinvader_api_delivery_carrier>=16.0dev,<16.1dev',
        'odoo-addon-shopinvader_delivery_carrier>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
