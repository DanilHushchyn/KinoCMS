from django.db.models import QuerySet
from src.booking.models import Seance
from src.booking.schemas.seance import SeanceFilterSchema


class SeanceService:
    """
    A service class for managing séances.
    """

    @staticmethod
    def get_filtered(filters: SeanceFilterSchema) -> list:
        """
        Get all séances.
        """
        result = Seance.objects.get_filtered(filters=filters)
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

    @staticmethod
    def get_by_id(seance_id: int) \
            -> Seance:
        """
        Get séance by id;
        :param seance_id for getting séance by id
        """
        seances = Seance.objects.get_by_id(seance_id=seance_id)
        return seances
