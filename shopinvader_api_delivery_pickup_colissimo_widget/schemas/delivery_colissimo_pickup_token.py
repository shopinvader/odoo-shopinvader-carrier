# Copyright 2024 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from extendable_pydantic import StrictExtendableBaseModel


class DeliveryColissimoPickupToken(StrictExtendableBaseModel):
    token: str
