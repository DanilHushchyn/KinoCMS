from django.db.models import QuerySet

from src.booking.models import Seance


class SeanceService:
    """
    A service class for managing séances.
    """

    @staticmethod
    def get_all() -> QuerySet[Seance]:
        """
        Get all séances.
        """
        seances = Seance.objects.get_all()
        return seances
