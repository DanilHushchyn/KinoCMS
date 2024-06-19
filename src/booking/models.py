from django.db import models


# Create your models here.
class Seance(models.Model):
    price = models.PositiveIntegerField()
    date = models.DateTimeField()
    hall = models.ForeignKey('cinemas.Hall', on_delete=models.CASCADE)
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Seance"
        verbose_name_plural = "Seances"
        db_table = 'seances'


class Ticket(models.Model):
    seance = models.ForeignKey('Seance', on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        db_table = 'tickets'
