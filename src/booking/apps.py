"""App for Booking Tickets on Séances
Help to manage with tickets and séances in system
"""

from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.booking"
