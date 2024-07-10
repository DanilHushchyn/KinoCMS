# -*- coding: utf-8 -*-
import copy
import json
import os
import random
from datetime import timedelta
from typing import Dict
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import date_time, phone_number
from src.booking.models import Seance, Ticket
from src.cinemas.models import Cinema, Hall
from src.core.models import Image, Gallery
from src.movies.models import (Movie, MovieParticipantRole,
                               MovieParticipantPerson, MovieParticipant,
                               Tech)
from src.pages.models import (TopSlider, BottomSlider,
                              TopSliderItem, BottomSliderItem,
                              ETEndBBanner, NewsPromo, Page, Tag)
from src.users.models import User
from pytils.translit import slugify
from django_countries.data import COUNTRIES


class Command(BaseCommand):
    _fake_ru = Faker("ru_RU")
    _fake_en = Faker("en_US")
    _fake_uk = Faker("uk_UA")
    _fake_uk.add_provider(phone_number)
    _fake_uk.add_provider(date_time)
    _cities = [key for key, _ in User.CITIES_CHOICES]

    def handle(self, null=None, *args, **options):
        self._create_superuser()
        self._create_users()
        self._create_techs()
        self._create_cinemas()
        self._create_halls()
        self._create_participants()
        self._create_movies()
        self._create_sliders()
        self._create_tags()
        self._create_news_promos()
        self._create_pages()

    @classmethod
    def _create_superuser(cls):
        if not User.objects.exists():
            user = User.objects.create(
                first_name=cls._fake_uk.first_name_male(),
                last_name=cls._fake_uk.last_name_male(),
                email="user@example.com",
                nickname=cls._fake_en.first_name().lower(),
                city=random.choice(cls._cities),
                address=cls._fake_uk.address(),
                man=random.choice([True, False]),
                phone_number=f'+3809{cls._fake_uk.msisdn()[4:]}',
                birthday=cls._fake_uk.date_of_birth(),
                is_superuser=True,
                is_staff=True,
                is_active=True,
            )
            user.set_password("Sword123*")
            user.save()

    @classmethod
    def _create_techs(cls):
        if not Tech.objects.exists():
            techs = [
                Tech(name='Cinetech', color="#AD0076"),
                Tech(name='Cinetech+', color="#DF1B66"),
                Tech(name='IMAX', color="#0F9539"),
                Tech(name='4DX', color="#514BBE"),
                Tech(name="RE'LUX", color="#4751FF"),
                Tech(name='IMAX with Laser', color="#FF1F1F"),
            ]
            Tech.objects.bulk_create(techs)

    @classmethod
    def _create_users(cls):
        if User.objects.count() == 1:
            users = []
            for i in range(101):
                first_name = cls._fake_en.first_name()
                email = f"{first_name.lower()}0{i}@example.com"
                user = User(
                    first_name=cls._fake_uk.first_name(),
                    last_name=cls._fake_uk.last_name(),
                    email=email,
                    nickname=cls._fake_en.first_name().lower(),
                    city=random.choice(cls._cities),
                    address=cls._fake_uk.address(),
                    man=random.choice([True, False]),
                    phone_number=f'+3809{cls._fake_uk.msisdn()[4:]}',
                    birthday=cls._fake_uk.date_of_birth(),
                    is_superuser=False,
                    is_staff=False,
                    is_active=True,
                )
                user.set_password('Sword123*')
                users.append(user)
            User.objects.bulk_create(users)

    @classmethod
    def _create_sliders(cls):
        if not TopSlider.objects.exists():
            slider = TopSlider.objects.create(active=True, speed=30)
            if not TopSliderItem.objects.exists():
                items = []
                for i in range(1, 6):
                    item = TopSliderItem(
                        url='https://www.youtube.com/',
                        image=cls._create_image('top_slider'),
                        text_uk=f'Заголовок для слайдера - {i}',
                        text_ru=f'Заголовок для слайдера - {i}',
                        slider=slider,
                    )
                    items.append(item)
                TopSliderItem.objects.bulk_create(items)

        if not BottomSlider.objects.exists():
            slider = BottomSlider.objects.create(active=True, speed=30)
            if not BottomSliderItem.objects.exists():
                items = []
                for i in range(1, 6):
                    item = BottomSliderItem(
                        url='https://www.youtube.com/',
                        image=cls._create_image('bottom_slider'),
                        slider=slider,

                    )
                    items.append(item)
                BottomSliderItem.objects.bulk_create(items)
        if not ETEndBBanner.objects.exists():
            ETEndBBanner.objects.create(
                color='#FFFFFF',
                use_img=False,
                image=cls._create_image('bottom_slider')
            )

    @classmethod
    def _create_image(cls, seed_path: str) -> Image:
        """
        Create image in db
        :param seed_path: path to seeds with images
        :return: Image model instance
        """
        random_image = random.choice(os.listdir(
            os.path.join("seed", seed_path)))
        image = open(os.path.join("seed", seed_path, random_image), "rb")
        image = Image.objects.create(
            alt='alt',
            image=File(image, "/media/" + image.name),
        )
        return image

    @classmethod
    def _create_gallery(cls, seed_path: str) -> Gallery:
        """
        Create gallery in db
        :param seed_path: path to seeds with images
        :return: Gallery model instance
        """
        gallery = Gallery.objects.create()
        for i in range(5):
            image = cls._create_image(seed_path)
            gallery.images.add(image)
        return gallery

    @classmethod
    def _create_cinemas(cls):
        if not Cinema.objects.exists():
            cinemas = []
            for i in range(1, 11):
                name_uk = f'Кінотеатр-0{i}'
                name_ru = f'Кинотеатр-0{i}'
                slug = slugify(name_uk)
                description_uk = cls._fake_uk.text(max_nb_chars=2500)
                description_ru = cls._fake_ru.text(max_nb_chars=2500)
                cinema = Cinema(
                    name_uk=name_uk,
                    name_ru=name_ru,
                    slug=slug,
                    email=f"cinema0{i}@example.com",
                    description_uk=description_uk,
                    description_ru=description_ru,
                    terms_uk={},
                    terms_ru={},
                    phone_1=f'+3809{cls._fake_uk.msisdn()[4:]}',
                    phone_2=f'+3809{cls._fake_uk.msisdn()[4:]}',
                    seo_title=name_uk,
                    seo_description=description_uk[:150],
                    seo_image=cls._create_image('cinema/banner'),
                    banner=cls._create_image('cinema/banner'),
                    logo=cls._create_image('cinema/logo'),
                    address_uk=cls._fake_uk.address(),
                    address_ru=cls._fake_ru.address(),
                    coordinate='https://www.google.com/maps/embed?pb='
                               '!1m14!1m12!1m3!1d5116.389570406765!2d8'
                               '.931456587933337!3d50.12007695809966'
                               '!2m3!1f0!2f0!3f0!3m2!'
                               '1i1024!2i768!4f13.1!5e0!3m2'
                               '!1sru!2sde!4v1718102814971!5m2!1sru!2sde',
                    gallery=cls._create_gallery('cinema/gallery'),
                )
                cinemas.append(cinema)
            Cinema.objects.bulk_create(cinemas)

    @classmethod
    def create_hall_schema(cls) -> Dict:
        random_schema = random.choice(os.listdir(
            os.path.join("seed", 'hall_schemas')))
        schema = open(os.path.join("seed", 'hall_schemas', random_schema), "rb")
        # Open the file in read mode
        with open(schema.name, "r") as f:
            # Read the entire content of the file
            data = f.read()
        # Parse the JSON string into a Python dictionary
        data_dict = json.loads(data)
        return data_dict

    @classmethod
    def _create_halls(cls):
        if not Hall.objects.exists():
            halls = []
            cinemas = Cinema.objects.all()
            for cinema in cinemas:
                for i in range(1, 4):
                    description_uk = cls._fake_uk.text(max_nb_chars=2500)
                    description_ru = cls._fake_ru.text(max_nb_chars=2500)
                    techs = list(Tech.objects.values_list('id', flat=True))
                    hall = Hall(
                        number=f'0{i}',
                        description_uk=description_uk,
                        description_ru=description_ru,
                        cinema=cinema,
                        tech_id=random.choice(techs),
                        seo_title=f'0{i}',
                        layout=cls.create_hall_schema(),
                        seo_description=description_uk[:150],
                        seo_image=cls._create_image('hall/banner'),
                        banner=cls._create_image('hall/banner'),
                        gallery=cls._create_gallery('hall/gallery'),
                    )
                    halls.append(hall)
            Hall.objects.bulk_create(halls)

    @classmethod
    def _create_tags(cls):
        if not Tag.objects.exists():
            tags = []
            for i in range(1, 50):
                name_uk = f'тег-0{i}'
                name_ru = f'тег-0{i}'
                color = random.choice(["494c8f", "faf0d7", "fadfd7",
                                       "c7c1f5", "f97420", "fbb00c",
                                       "2aae80", "ffa9d2", "fb380c"])
                tag = Tag(
                    name_uk=name_uk,
                    name_ru=name_ru,
                    color=color,
                )
                tags.append(tag)
            Tag.objects.bulk_create(tags)

    @classmethod
    def _create_news_promos(cls):
        if not NewsPromo.objects.exists():
            news_promos = []
            for i in range(1, 101):
                if i % 2 == 0:
                    promo = True
                    name_uk = f'Акція - 0{i}'
                    name_ru = f'Акция - 0{i}'
                else:
                    name_uk = f'Новина - 0{i}'
                    name_ru = f'Новость - 0{i}'
                    promo = False
                description_uk = (cls._fake_uk.text(max_nb_chars=2500)
                                  .capitalize())
                description_ru = (cls._fake_ru.text(max_nb_chars=2500)
                                  .capitalize())
                news_promo = NewsPromo(
                    name_uk=name_uk,
                    name_ru=name_ru,
                    slug=slugify(name_uk),
                    description_uk=description_uk,
                    description_ru=description_ru,
                    video_link="https://www.youtube.com/",
                    promo=promo,
                    active=True,
                    seo_title=name_uk,
                    seo_description=description_uk[:150],
                    seo_image=cls._create_image('news_promo'),
                    banner=cls._create_image('news_promo'),
                    gallery=cls._create_gallery('news_promo'),
                )
                news_promos.append(news_promo)
            news_promos = NewsPromo.objects.bulk_create(news_promos)
            tag_ids = list(Tag.objects
                           .values_list('id', flat=True))
            for news_promo in news_promos:
                news_promo_tags = random.sample(tag_ids, 3)
                news_promo.tags.set(news_promo_tags)
                news_promo.save()

    @classmethod
    def _create_pages(cls):
        if not Page.objects.exists():
            pages = []
            for i in range(1, 21):
                name_uk = f'Сторінка - 0{i}'
                name_ru = f'Страница - 0{i}'
                can_delete = True
                if i in [1, 2, 3, 4, 5]:
                    can_delete = False
                page = Page(
                    name_uk=name_uk,
                    name_ru=name_ru,
                    slug=slugify(name_uk),
                    content_uk={},
                    content_ru={},
                    active=True,
                    can_delete=can_delete,
                    seo_title=name_uk,
                    seo_description=name_uk,
                    seo_image=cls._create_image('cinema/banner'),
                    banner=cls._create_image('cinema/banner'),
                    gallery=cls._create_gallery('cinema/gallery'),
                )
                pages.append(page)
            Page.objects.bulk_create(pages)

    @classmethod
    def _create_schedule(cls, start_date, end_date, movie, price, hall_id):
        import zoneinfo
        tzinfo = zoneinfo.ZoneInfo('Europe/Kiev')
        seances = []
        for i in range(1, 31):
            date = cls._fake_uk.date_time_between(start_date=start_date,
                                                  end_date=end_date,
                                                  tzinfo=tzinfo)
            seance = Seance(
                movie=movie,
                price=price,
                hall_id=hall_id,
                date=date,
            )
            seances.append(seance)
        Seance.objects.bulk_create(seances)

    @classmethod
    def _create_seances(cls, movie: Movie):
        if not movie.seance_set.exists():
            import zoneinfo
            hall_ids = list(Hall.objects.values_list('id', flat=True))
            for hall_id in hall_ids:
                price = random.choice([150, 100, 250, 500, 280,
                                       180, 600, 350, 420])
                start_date = movie.released
                end_date = movie.released + timedelta(days=30)
                cls._create_schedule(start_date=start_date,
                                     end_date=end_date,
                                     movie=movie,
                                     hall_id=hall_id,
                                     price=price)

                start_date = movie.released + timedelta(days=30)
                end_date = movie.released + timedelta(days=60)
                cls._create_schedule(start_date=start_date,
                                     end_date=end_date,
                                     movie=movie,
                                     hall_id=hall_id,
                                     price=price)

                start_date = movie.released + timedelta(days=60)
                end_date = movie.released + timedelta(days=90)
                cls._create_schedule(start_date=start_date,
                                     end_date=end_date,
                                     movie=movie,
                                     hall_id=hall_id,
                                     price=price)



    @classmethod
    def _create_participants(cls) -> None:
        """
        Create participants in db
        :return: None
        """
        if not MovieParticipantRole.objects.exists():
            MovieParticipantRole.objects.bulk_create(
                [
                    MovieParticipantRole(name_uk='актор',
                                         name_ru='актёр'),
                    MovieParticipantRole(name_uk='продюсер',
                                         name_ru='продюсер'),
                    MovieParticipantRole(name_uk='режисер',
                                         name_ru='режисёр'),
                    MovieParticipantRole(name_uk='сценарист',
                                         name_ru='сценарист'),
                    MovieParticipantRole(name_uk='композитор',
                                         name_ru='композитор'),
                ]
            )
        role_ids = list(MovieParticipantRole.objects
                        .values_list('id', flat=True))
        if not MovieParticipantPerson.objects.exists():
            persons = []
            for i in range(1, 31):
                person = MovieParticipantPerson(
                    fullname_uk=cls._fake_uk.name_nonbinary(),
                    fullname_ru=cls._fake_ru.name_nonbinary(),
                )
                persons.append(person)
            MovieParticipantPerson.objects.bulk_create(persons)
        person_ids = list(MovieParticipantPerson.objects
                          .values_list('id', flat=True))
        if not MovieParticipant.objects.exists():
            participants = []
            for person_id in person_ids:
                participants.append(
                    MovieParticipant(
                        role_id=random.choice(role_ids),
                        person_id=person_id
                    )
                )
            MovieParticipant.objects.bulk_create(participants)

    @classmethod
    def _create_movies(cls):
        if not Movie.objects.exists():
            movies = []
            for i in range(1, 41):
                name_uk = f'Фільм-0{i}'
                name_ru = f'Фильм-0{i}'
                slug = slugify(f"movie-0{i}")
                description_uk = (cls._fake_uk.text(max_nb_chars=2500)
                                  .capitalize())
                description_ru = (cls._fake_ru.text(max_nb_chars=2500)
                                  .capitalize())
                if i % 2 == 0:
                    released = (cls._fake_uk
                                .date_this_month(before_today=True,
                                                 after_today=False))
                else:
                    released = (cls._fake_uk
                                .date_this_month(before_today=False,
                                                 after_today=True))
                hour = random.choice(["01", "02", "03"])
                minutes = random.choice(["15", "25", "30", "00", "40"])
                year = random.choice([2024, 2020, 2015, 2017, 2012, 2018, 2019])
                movie = Movie(
                    name_uk=name_uk,
                    name_ru=name_ru,
                    slug=slug,
                    description_uk=description_uk,
                    description_ru=description_ru,
                    year=year,
                    budget=i * 1_000_0000,
                    duration=f"{hour}:{minutes}",
                    countries=random.sample(list(COUNTRIES.keys()), 4),
                    genres=random.sample([key for key, _ in Movie.GENRES_CHOICES], 2),
                    legal_age=random.choice([key for key, _ in Movie.AGE_CHOICES]),
                    released=released,
                    trailer_link='https://youtu.be/TCwmXY_f-e0?si=RWFigjQf7sCj3ngb',
                    seo_title=name_uk,
                    seo_description=description_uk[:150],
                    seo_image=cls._create_image('movie/card'),
                    card_img=cls._create_image('movie/card'),
                    gallery=cls._create_gallery('movie/gallery'),
                )
                movies.append(movie)
            movies = Movie.objects.bulk_create(movies)
            participant_ids = list(MovieParticipant.objects
                                   .values_list('id', flat=True))
            tech_ids = list(Tech.objects.values_list('id', flat=True))

            for movie in movies:
                movie_participants = random.sample(participant_ids, 3)
                movie.participants.set(movie_participants)
                movie_techs = random.sample(tech_ids, 2)
                movie.techs.set(movie_techs)
                movie.save()
                cls._create_seances(movie)

    # @classmethod
    # def _create_tickets(cls):
    #     if not Ticket.objects.exists():
    #         movies = Movie.objects.prefetch_related('seance_set').all()
    #         for movie in movies:
    #             seances = movie.seance_set.all()
    #             # num_seances = random.randrange(1, len(seance_ids), 1)
    #             # print(num_seances, len(seance_ids[:num_seances]), movie.id)
    #
    #             for seance in seances:
    #                 if random.choice([True, False, False]):
    #                     rows = seance.hall.layout['rows']
    #                     rows = copy.deepcopy(rows)
    #                     for i, row in enumerate(rows):
    #                         if 'number' not in row:
    #                             if rows[i]:
    #                                 del rows[i]
    #                     rows_len = len(rows)
    #                     row = random.randrange(1, rows_len, 1)
    #                     for item in seance.hall.layout['rows']
    #                     seats = seance.hall.layout['rows'][row]['seats']
    #                     seats = copy.deepcopy(seats)
    #                     for i, seat in enumerate(seats):
    #                         if 'number' not in seat:
    #                             if seats[i]:
    #                                 del seats[i]
    #                     seats_len = len(seance.hall.layout['rows'][row]['seats'])
    #
    #                     seat = random.randrange(1, seats_len, 1)
    #                     print(row, seat)
    #                     # for row in seance.hall.layout['rows']:
    #                     #     if 'number' in row and row['number'] == ticket.row:
    #                     #         for seat in row['seats']:
    #                     #             if ('number' in seat and
    #                     #                     seat['number'] == ticket.seat):
    #                     #                 found = True
    #                     # if found is False:
