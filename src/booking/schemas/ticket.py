from typing import List
from ninja import Schema


class TicketSchema(Schema):
    """
    Pydantic schema for sending ticket's location data.
    """
    row: int
    seat: int


class BuyTicketSchema(Schema):
    """
    Pydantic schema for buying tickets.
    """
    seance_id: int
    tickets: List[TicketSchema]
