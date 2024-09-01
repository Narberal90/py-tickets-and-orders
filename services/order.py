import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Ticket, Order, MovieSession


@transaction.atomic
def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: Optional[str] = None
) -> None:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    ticket_objects = [
        Ticket(order=order,
               row=ticket["row"],
               seat=ticket["seat"],
               movie_session_id=ticket["movie_session"]) for ticket in tickets
    ]

    Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: Optional[str] = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        user = get_user_model().objects.get(username=username)
        orders = orders.filter(user=user)

    return orders

