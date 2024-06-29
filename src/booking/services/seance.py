from django.db.models import QuerySet

from src.booking.models import Seance
from django.utils import timezone


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
        today = timezone.now()
        seances = seances.filter(date__date=today.date())
        result = [{
         "date": str(today),
         "seances": seances,
        }]
        return result

    @staticmethod
    def get_today_seances(cnm_slug: str, hall_id: int) \
            -> QuerySet[Seance]:
        """
        Get séances queryset for today;
        :param cnm_slug for filtering séances by cinema
        :param hall_id for filtering séances by hall
        """
        seances = Seance.objects.get_today_seances(cnm_slug=cnm_slug,
                                                   hall_id=hall_id)
        return seances
