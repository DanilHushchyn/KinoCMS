import pendulum
from django.db.models import Sum

from src.booking.models import Ticket
from src.movies.models import Tech
from src.users.models import User


class StatisticService:
    """A service class for managing images."""

    def __init__(self):
        self.image_types = [
            "jpeg",
            "jpg",
            "png",
            "svg",
            "webp",
        ]

    @staticmethod
    def progress_calc(first_number: int, second_number: int) -> float:
        if first_number is None:
            first_number = 0
        if second_number is None:
            second_number = 0
        if second_number <= 0:
            return 0
        return ((first_number / second_number) * 100) - 100

    @staticmethod
    def convert_to_percent(value: int, total: int) -> float:
        if value is None:
            value = 0
        if total is None:
            total = 0
        if total <= 0:
            return 0
        return round(((value / total) * 100), 2)

    def get_computed_nums(
        self,
    ) -> dict:
        """Get computed numbers of statistic for our site."""
        today = pendulum.now(tz="Europe/Kiev")
        start_current_month = today.start_of("month")
        end_current_month = today.end_of("month")
        start_last_month = start_current_month.subtract(months=1)
        end_last_month = end_current_month.subtract(months=1)
        users = User.objects.all()
        users_count = users.count()
        men = users.filter(man=True).count()
        women = users.filter(man=False).count()
        current_month_tickets = Ticket.objects.filter(
            date_created__range=[start_current_month, end_current_month],
        )
        current_month_income = current_month_tickets.aggregate(
            total_income=Sum("seance__price")
        )["total_income"]
        last_month_tickets = Ticket.objects.filter(
            date_created__range=[start_last_month, end_last_month],
        )
        last_month_income = last_month_tickets.aggregate(
            total_income=Sum("seance__price")
        )["total_income"]
        income_progress = self.progress_calc(current_month_income, last_month_income)
        income_progress = 0 if income_progress is None else round(income_progress, 2)
        result = {
            "current_month_income": int(current_month_income or 0),
            "income_progress": income_progress,
            "users_count": int(users_count or 0),
            "men": int(men or 0),
            "women": int(women or 0),
        }
        return result

    def get_most_popular_movies(
        self,
    ) -> dict:
        """Get most popular movies on the site."""
        today = pendulum.now(tz="Europe/Kiev")
        start_current_month = today.start_of("month")
        tickets = Ticket.objects.prefetch_related("seance__movie").filter(
            date_created__gte=start_current_month
        )
        labels = []
        for ticket in tickets:
            labels.append(ticket.seance.movie.name_uk)
        labels = list(set(labels))
        values = []
        for label in labels:
            value = tickets.filter(seance__movie__name_uk=label).count()

            values.append(value)
        result = {"labels": labels, "values": values}
        return result

    def get_most_income_movies(
        self,
    ) -> dict:
        """Get most income movies on the site."""
        today = pendulum.now(tz="Europe/Kiev")
        start_current_month = today.start_of("month")
        tickets = Ticket.objects.prefetch_related("seance__movie").filter(
            date_created__gte=start_current_month
        )
        labels = []
        for ticket in tickets:
            labels.append(ticket.seance.movie.name_uk)
        labels = list(set(labels))
        values = []
        for label in labels:
            value = tickets.filter(seance__movie__name_uk=label).aggregate(
                total_income=Sum("seance__price")
            )

            values.append(value["total_income"])
        result = {"labels": labels, "values": values}
        return result

    def get_most_popular_techs(
        self,
    ) -> dict:
        """Get most popular techs on the site."""
        today = pendulum.now(tz="Europe/Kiev")
        start_current_month = today.start_of("month")
        tickets = Ticket.objects.prefetch_related(
            "seance__movie", "seance__hall__tech"
        ).filter(date_created__gte=start_current_month)
        techs = Tech.objects.all()
        labels = [tech.name for tech in techs]
        values = []
        for label in labels:
            value = tickets.filter(seance__hall__tech__name=label).count()
            values.append(value)
        total = sum(values)
        values_percents = []
        for value in values:
            value = self.convert_to_percent(value, total)
            values_percents.append(value)
        result = {"labels": labels, "values": values_percents}
        return result
