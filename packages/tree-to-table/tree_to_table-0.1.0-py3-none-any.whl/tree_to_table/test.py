from typing import Dict, List

from .mappers import Get, Apply, Choice, Mapper
from .table import Table, Column
from .transforms import one_to_many


def choose_participant(participant_id: str):
    def choose(charge_items: List[Dict]):
        for charge_item in charge_items:
            if charge_item["participant_id"] == participant_id:
                return charge_item

    return choose


# TODO: We could exhaust with zip, but we could also cross product on one to many
# @one_to_many({"invoice_item": Get("service_id")})
class Invoice(Table):
    service_id: Mapper = Get("service_id")
    patient_id: Mapper = Get("patient_id")
    patient_name: Mapper = Get(
        "charge_items", Choice(choose_participant("patient"), Get("name"))
    )


print(
    Invoice.transform(
        99999999
        * [
            {
                "yeets": [1, 2, 3],
                "service_id": 1,
                "patient_id": 2,
                "charge_items": [
                    {"participant_id": "ya mum", "name": "ya mum"},
                    {"participant_id": "patient", "name": "james"},
                ],
            }
        ]
    )
)
