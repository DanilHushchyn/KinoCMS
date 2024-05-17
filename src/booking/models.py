from django.db import models


# Create your models here.
class Seance(models.Model):
    slug = models.SlugField(db_index=True, unique=True, null=True)

    tech_type = models.CharField(max_length=60)
    price = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    hall = models.ForeignKey('cinemas.Cinema', on_delete=models.CASCADE, null=True)

    # hall = models.ForeignKey('cinemas.Cinema', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Seance"
        verbose_name_plural = "Seances"
        db_table = 'seances'


class Ticket(models.Model):
    seance = models.ForeignKey('Seance', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    row = models.PositiveIntegerField(null=True)
    seat = models.PositiveIntegerField(null=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        db_table = 'tickets'