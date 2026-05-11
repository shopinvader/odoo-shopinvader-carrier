# Copyright 2026 Akretion (http://www.akretion.com).
# @author Florian Mounier <florian.mounier@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime

pickup_sites = {
    "quality": 2,
    "sites": [
        {
            "city": "VILLEURBANNE",
            "country": "FR",
            "details": "",
            "disabled_access": False,
            "distance": 172,
            "hours": {
                "friday": [{"end": datetime.time(21, 0), "start": datetime.time(7, 0)}],
                "monday": [{"end": datetime.time(21, 0), "start": datetime.time(7, 0)}],
                "saturday": [
                    {"end": datetime.time(21, 0), "start": datetime.time(7, 0)}
                ],
                "sunday": [],
                "thursday": [
                    {"end": datetime.time(21, 0), "start": datetime.time(7, 0)}
                ],
                "tuesday": [
                    {"end": datetime.time(21, 0), "start": datetime.time(7, 0)}
                ],
                "wednesday": [
                    {"end": datetime.time(21, 0), "start": datetime.time(7, 0)}
                ],
            },
            "id": "060567",
            "lat": "45.7695505",
            "lng": "4.86314559",
            "max_weight": 30000,
            "name": "BUREAU DE POSTE VILLEURBANNE BELLECOMBE RP",
            "parking": False,
            "street": "13 RUE BELLECOMBE\nCARREFOUR CITY",
            "type": "BPR",
            "vacations": [
                {
                    "end": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
            ],
            "zip": "69100",
            "zone": "R01",
        },
        {
            "city": "VILLEURBANNE",
            "country": "FR",
            "details": "",
            "disabled_access": True,
            "distance": 241,
            "hours": {
                "friday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
                "monday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
                "saturday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)}
                ],
                "sunday": [],
                "thursday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
                "tuesday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
                "wednesday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
            },
            "id": "699370",
            "lat": "45.770698",
            "lng": "4.866231",
            "max_weight": 30000,
            "name": "BUREAU DE POSTE VILLEURBANNE LES CHARPENNES",
            "parking": False,
            "street": "38 COURS EMILE ZOLA",
            "type": "BPR",
            "vacations": [
                {
                    "end": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
            ],
            "zip": "69100",
            "zone": "R01",
        },
        {
            "city": "LYON",
            "country": "FR",
            "details": "",
            "disabled_access": True,
            "distance": 983,
            "hours": {
                "friday": [{"end": datetime.time(18, 0), "start": datetime.time(9, 0)}],
                "monday": [{"end": datetime.time(18, 0), "start": datetime.time(9, 0)}],
                "saturday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)}
                ],
                "sunday": [],
                "thursday": [
                    {"end": datetime.time(18, 0), "start": datetime.time(9, 0)}
                ],
                "tuesday": [
                    {"end": datetime.time(18, 0), "start": datetime.time(9, 0)}
                ],
                "wednesday": [
                    {"end": datetime.time(18, 0), "start": datetime.time(9, 0)}
                ],
            },
            "id": "693330",
            "lat": "45.763599",
            "lng": "4.856477",
            "max_weight": 30000,
            "name": "BUREAU DE POSTE LYON LAFAYETTE",
            "parking": False,
            "street": "168 COURS LAFAYETTE",
            "type": "BPR",
            "vacations": [
                {
                    "end": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
            ],
            "zip": "69003",
            "zone": "R01",
        },
        {
            "city": "VILLEURBANNE",
            "country": "FR",
            "details": "",
            "disabled_access": True,
            "distance": 1057,
            "hours": {
                "friday": [{"end": datetime.time(12, 0), "start": datetime.time(9, 0)}],
                "monday": [{"end": datetime.time(12, 0), "start": datetime.time(9, 0)}],
                "saturday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)}
                ],
                "sunday": [],
                "thursday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)}
                ],
                "tuesday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)}
                ],
                "wednesday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)}
                ],
            },
            "id": "699380",
            "lat": "45.763796",
            "lng": "4.871894",
            "max_weight": 30000,
            "name": "BUREAU DE POSTE VILLEURBANNE TOTEM BP",
            "parking": False,
            "street": "13 B COURS TOLSTOI",
            "type": "BPR",
            "vacations": [
                {
                    "end": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
            ],
            "zip": "69100",
            "zone": "R01",
        },
        {
            "city": "LYON",
            "country": "FR",
            "details": "",
            "disabled_access": True,
            "distance": 1143,
            "hours": {
                "friday": [
                    {"end": datetime.time(12, 30), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
                "monday": [
                    {"end": datetime.time(12, 30), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
                "saturday": [
                    {"end": datetime.time(12, 0), "start": datetime.time(9, 0)}
                ],
                "sunday": [],
                "thursday": [
                    {"end": datetime.time(12, 30), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
                "tuesday": [
                    {"end": datetime.time(12, 30), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
                "wednesday": [
                    {"end": datetime.time(12, 30), "start": datetime.time(9, 0)},
                    {"end": datetime.time(18, 0), "start": datetime.time(14, 0)},
                ],
            },
            "id": "699200",
            "lat": "45.771097",
            "lng": "4.848447",
            "max_weight": 30000,
            "name": "BUREAU DE POSTE LYON SULLY",
            "parking": False,
            "street": "69 RUE SULLY",
            "type": "BPR",
            "vacations": [
                {
                    "end": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 6, 8, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 28, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 5, 7, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 30, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
                {
                    "end": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                    "start": datetime.datetime(
                        2025, 4, 20, 22, 0, tzinfo=datetime.timezone.utc
                    ),
                },
            ],
            "zip": "69006",
            "zone": "R01",
        },
    ],
}
