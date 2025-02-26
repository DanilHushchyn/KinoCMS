"""Movie Service for implementing movie logic on site"""

import datetime

from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext as _
from injector import inject

from src.core.management.commands.init_script import Command
from src.core.schemas.base import MessageOutSchema
from src.core.services.core import CoreService
from src.core.services.gallery import GalleryService
from src.core.services.images import ImageService
from src.core.utils import make_slug
from src.movies.models import Movie
from src.movies.models import MovieParticipant
from src.movies.models import MovieParticipantRole
from src.movies.models import Tech
from src.movies.schemas import MovieInSchema
from src.movies.schemas import MovieUpdateSchema


class MovieService:
    """A service class for managing movies."""

    @inject
    def __init__(
        self,
        image_service: ImageService,
        core_service: CoreService,
        gall_service: GalleryService,
    ):
        self.core_service = core_service
        self.image_service = image_service
        self.gall_service = gall_service

    def create(self, request: HttpRequest, schema: MovieInSchema) -> MessageOutSchema:
        """Create Movie."""
        self.core_service.check_field_unique(
            value=schema.name_uk, field_name="name_uk", model=Movie
        )
        self.core_service.check_field_unique(
            value=schema.name_ru, field_name="name_ru", model=Movie
        )
        bodies = [schema.card_img, schema.seo_image]
        card_img, seo_image = self.image_service.bulk_create(schemas=bodies)
        gallery = self.gall_service.create(images=schema.gallery)
        movie = Movie.objects.create(
            name_uk=schema.name_uk,
            name_ru=schema.name_ru,
            slug=make_slug(value=schema.name_uk, model=Movie),
            description_uk=schema.description_uk,
            description_ru=schema.description_ru,
            gallery=gallery,
            year=schema.year,
            legal_age=schema.legal_age.value,
            duration=schema.duration,
            budget=schema.budget,
            trailer_link=schema.trailer_link,
            card_img=card_img,
            released=schema.released,
            countries=schema.countries,
            genres=schema.genres,
            seo_title=schema.seo_title,
            seo_description=schema.seo_description,
            seo_image=seo_image,
        )
        if schema.participants is not None:
            movie.participants.set(schema.participants)
        if schema.techs is not None:
            movie.techs.set(schema.techs)
        movie.save()
        Command._create_seances(movie)
        return MessageOutSchema(detail=_("Фільм успішно створений"))

    def update(
        self, request: HttpRequest, mv_slug: str, schema: MovieUpdateSchema
    ) -> MessageOutSchema:
        """Update Movie."""
        movie = Movie.objects.get_by_slug(mv_slug=mv_slug)
        self.core_service.check_field_unique(
            value=schema.name_uk, field_name="name_uk", instance=movie, model=Movie
        )
        self.core_service.check_field_unique(
            value=schema.name_ru, field_name="name_ru", instance=movie, model=Movie
        )
        self.image_service.update(schema.card_img, movie.card_img)
        self.image_service.update(schema.seo_image, movie.seo_image)

        self.gall_service.update(schemas=schema.gallery, gallery=movie.gallery)
        expt_list = ["card_img", "seo_image", "gallery", "participants"]
        for attr, value in schema.dict().items():
            if attr not in expt_list and value is not None:
                setattr(movie, attr, value)

        if schema.participants is not None:
            movie.participants.set(schema.participants)

        movie.slug = make_slug(value=movie.name_uk, model=Movie, instance=movie)
        movie.save()
        return MessageOutSchema(detail=_("Фільм успішно оновлений"))

    @staticmethod
    def get_by_slug(mv_slug: str) -> Movie:
        """Get movie by slug."""
        movie = Movie.objects.get_by_slug(mv_slug=mv_slug)
        return movie

    @staticmethod
    def search(search_line: str) -> QuerySet[Movie]:
        """Get movies queryset by search_line."""
        movies = Movie.objects.get_by_search_line(search_line=search_line)
        return movies

    @staticmethod
    def get_today_movies() -> QuerySet[Movie]:
        """Get movies queryset with séances for today;"""
        movies = Movie.objects.get_today_movies()
        return movies

    @staticmethod
    def get_all(release: str) -> QuerySet:
        """Get all movies;
        :param release for sorting movie by release(soon or current) date
        """
        movie = Movie.objects.select_related("card_img").all()
        today = datetime.date.today()
        if release == "current":
            movie = movie.filter(released__lte=today)
        else:
            movie = movie.filter(released__gte=today)
        return movie

    @staticmethod
    def get_schedule_filter() -> QuerySet[Movie]:
        """Get all movies for filter in schedule in the client site;"""
        movies = Movie.objects.only("slug", "name")
        return movies

    @staticmethod
    def get_legal_ages() -> list:
        """Get all legal age choices for movie."""
        ages = Movie.AGE_CHOICES
        return ages

    @staticmethod
    def get_genres() -> list:
        """Get all genres for movie."""
        # keys = [k for k, v in Movie.GENRES_CHOICES]
        # print(keys)
        genres = Movie.GENRES_CHOICES
        return genres

    @staticmethod
    def get_techs() -> QuerySet[Tech]:
        """Get all techs for movie."""
        techs = Tech.objects.all()
        return techs

    @staticmethod
    def get_participants() -> QuerySet[MovieParticipant]:
        """Get all participants for movie."""
        participants = MovieParticipant.objects.prefetch_related("role", "person").all()
        return participants

    @staticmethod
    def get_participants_grouped() -> QuerySet[MovieParticipantRole]:
        """Get all participants for movie grouped by profession."""
        participants = MovieParticipant.objects.prefetch_related("role", "person").all()

        mv_roles = MovieParticipantRole.objects.all()
        for mv_role in mv_roles:
            persons_list = []
            for participant in participants:
                if participant.role == mv_role:
                    persons_list.append(participant)
            mv_role.persons = persons_list
        # mv_roles.mv_persons = mv_roles
        return mv_roles

    def delete_by_slug(self, mv_slug: str) -> MessageOutSchema:
        """Delete movie by slug."""
        movie = Movie.objects.get_by_slug(mv_slug=mv_slug)
        movie_imgs_ids = [movie.seo_image_id, movie.card_img_id]
        gall = movie.gallery
        movie.delete()
        gall_imgs_ids = gall.images.values_list("id", flat=True)
        gall.delete()
        gall_imgs_ids = list(gall_imgs_ids)
        imgs_ids_for_delete = movie_imgs_ids + gall_imgs_ids
        self.image_service.bulk_delete(imgs_ids_for_delete)
        return MessageOutSchema(detail=_("Фільм успішно видалений"))
