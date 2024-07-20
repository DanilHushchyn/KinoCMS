from django.db import models

from src.booking.managers.seance import SeanceManager
from src.booking.managers.ticket import TicketManager


# Create your models here.
class Seance(models.Model):
    """Сеансы на предстоящие фильмы"""

    price = models.PositiveIntegerField()
    date = models.DateTimeField()
    hall = models.ForeignKey("cinemas.Hall", on_delete=models.CASCADE)
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
    objects = SeanceManager()

    class Meta:
        ordering = ["date"]
        verbose_name = "Seance"
        verbose_name_plural = "Seances"
        db_table = "seances"


class Ticket(models.Model):
    """Билеты на предстоящие сеансы
    :param row номер ряда
    :param seat номер места
    """

    seance = models.ForeignKey("Seance", on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    objects = TicketManager()

    class Meta:
        unique_together = ("seance", "row", "seat")
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        db_table = "tickets"
