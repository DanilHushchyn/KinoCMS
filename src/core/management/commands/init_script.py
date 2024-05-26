# -*- coding: utf-8 -*-
import os
import random

from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import date_time,phone_number


from src.users.models import User

# fake = Faker()
# fake.add_provider(date_time)
# fake.add_provider(phone_number)


class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.fake_ru = Faker("ru_RU")
        self.fake_en = Faker("en_US")
        self.fake_uk = Faker("uk_UA")
        self.fake_uk.add_provider(phone_number)
        self.fake_uk.add_provider(date_time)
        cities = [key for key,value in User.CITIES_CHOICES]
        self.cities = cities

    def handle(self, null=None, *args, **options):
        self._create_superuser()
        self._create_users()

    def _create_superuser(self):
        user = User.objects.create(
            first_name=self.fake_uk.first_name_male(),
            last_name=self.fake_uk.last_name_male(),
            email="user@example.com",
            nickname=self.fake_en.first_name().lower(),
            city=random.choice(self.cities),
            address=self.fake_uk.address(),
            man=random.choice([True, False]),
            phone_number=f'+3809{self.fake_uk.msisdn()[4:]}',
            birthday=self.fake_uk.date_of_birth(),
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password("Sword123*")
        user.save()

    def _create_users(self):
        for i in range(100):
            first_name = self.fake_en.first_name()
            last_name = self.fake_en.last_name()
            domain_name = self.fake_en.domain_name()

            email = (f"{first_name}.{last_name}@{domain_name}"
                     .lower())
            user = User.objects.create(
                first_name=self.fake_uk.first_name(),
                last_name=self.fake_uk.first_name(),
                email=email,
                nickname=self.fake_en.first_name().lower(),
                city=random.choice(self.cities),
                address=self.fake_uk.address(),
                man=random.choice([True, False]),
                phone_number=f'+3809{self.fake_uk.msisdn()[4:]}',
                birthday=self.fake_uk.date_of_birth(),
                is_superuser=False,
                is_staff=False,
                is_active=True,
            )
            user.set_password("Sword123*")
            user.save()
    #
    # def _create_games(self):
    #     for i in range(3):
    #         random_filter_logo = random.choice(os.listdir(os.path.join("seed", "filter_logo")))
    #         random_product_logo = random.choice(os.listdir(os.path.join("seed", "product_logo")))
    #         filter_logo = open(os.path.join("seed", "filter_logo", random_filter_logo), "rb")
    #         product_logo = open(os.path.join("seed", "product_logo", random_product_logo), "rb")
    #         game = Game.objects.create(
    #             name=self.fake_en.unique.word().capitalize(),
    #             logo_filter=File(filter_logo, "/media/" + filter_logo.name),
    #             logo_product=File(product_logo, "/media/" + product_logo.name),
    #             logo_product_alt_en=self.fake_en.word(),
    #             logo_product_alt_uk=self.fake_uk.word(),
    #             logo_filter_alt_en=self.fake_en.word(),
    #             logo_filter_alt_uk=self.fake_uk.word(),
    #             order=i,
    #         )
    #         game.save()
    #
    # def _create_teams(self):
    #     random_team_img = random.choice(os.listdir(os.path.join("seed", "team")))
    #     team_img = open(os.path.join("seed", "team", random_team_img), "rb")
    #     Team.objects.create(
    #         team_img=File(team_img, "/media/" + team_img.name),
    #         team_img_alt_en="Alliance",
    #         team_img_alt_uk="Альянс",
    #     )
    #     Team.objects.create(
    #         team_img=File(team_img, "/media/" + team_img.name),
    #         team_img_alt_en="Horde",
    #         team_img_alt_uk="Орда",
    #     )
    #
    # def _create_calendar(self):
    #     calendar = Calendar.objects.create(title="Calendar")
    #     for i in range(3):
    #         block = CalendarBlock.objects.create(
    #             title_en=self.fake_en.word().capitalize(),
    #             title_uk=self.fake_uk.word().capitalize(),
    #             subtitle_en=self.fake_en.word().capitalize(),
    #             subtitle_uk=self.fake_uk.word().capitalize(),
    #             calendar=calendar,
    #         )
    #         for j in range(4):
    #             team1 = Team.objects.first()
    #             team2 = Team.objects.last()
    #             CalendarBlockItem.objects.create(
    #                 date=self.fake_en.date(),
    #                 team1_from=self.fake_en.time(),
    #                 team1_until=self.fake_en.time(),
    #                 team2_from=self.fake_en.time(),
    #                 team2_until=self.fake_en.time(),
    #                 block=block,
    #                 team1=team1,
    #                 team2=team2,
    #             )
    #
    # def _create_pages(self):
    #     for game in Game.objects.all():
    #         for j in range(5):
    #             worth_look = WorthLook.objects.create(
    #                 title=self.fake_en.word().capitalize(),
    #             )
    #             calendar = Calendar.objects.first()
    #             page = CatalogPage.objects.create(
    #                 title_en=self.fake_en.word().capitalize(),
    #                 title_uk=self.fake_uk.word().capitalize(),
    #                 description_en=self.fake_en.text(max_nb_chars=500).capitalize(),
    #                 description_uk=self.fake_uk.text(max_nb_chars=500).capitalize(),
    #                 parent=None,
    #                 game=game,
    #                 order=j,
    #                 worth_look=worth_look,
    #                 calendar=calendar,
    #             )
    #             for i in range(4):
    #                 CatalogTabs.objects.create(
    #                     title_en=self.fake_en.word().capitalize(),
    #                     title_uk=self.fake_uk.word().capitalize(),
    #                     content_en=self.fake_en.text(max_nb_chars=500).capitalize(),
    #                     content_uk=self.fake_uk.text(max_nb_chars=500).capitalize(),
    #                     order=i,
    #                     catalog_id=page.id,
    #                 )
    #     for item in WorthLook.objects.all():
    #         item: WorthLook
    #         ids = CatalogPage.objects.values_list("id", flat=True)
    #         for i in range(4):
    #             random_card_image = random.choice(os.listdir(os.path.join("seed", "card_image")))
    #             card_image = open(os.path.join("seed", "card_image", random_card_image), "rb")
    #             WorthLookItem.objects.create(
    #                 image=File(card_image, "/media/" + card_image.name),
    #                 image_alt_en=self.fake_en.word(),
    #                 image_alt_uk=self.fake_uk.word(),
    #                 carousel=item,
    #                 catalog_page_id=random.choice(ids),
    #             )
    #
    # def _create_main_page(self):
    #     obj = {
    #         "instagram_nickname": "@gold_bost",
    #         "instagram_link": "https://www.youtube.com/",
    #         "facebook_link": "https://www.youtube.com/",
    #         "reddit_link": "https://www.youtube.com/",
    #         "email": "user@example.com",
    #         "discord_link": "https://www.youtube.com/",
    #         "whats_up_link": "https://www.youtube.com/",
    #         "footer_bottom_text": "© 2020. All rights reserved",
    #         "privacy_policy_link": "https://www.youtube.com/",
    #         "terms_of_use_link": "https://www.youtube.com/",
    #         "refund_policy_link": "https://www.youtube.com/",
    #         "subscribe_sale": 10,
    #         "address1_en": "Ukraine, Odessa, st. Kosmonavtov, 32",
    #         "address1_uk": "Українa, м. Одеса, вул. Космонавтів, 32",
    #         "address2_en": "Ukraine, Odessa, st. Kosmonavtov, 32",
    #         "address2_uk": "Українa, м. Одеса, вул. Космонавтів, 32",
    #         "footer_description_en": "We cooperate only with qualified and experienced top world players who participate "
    #         "personally in each event and ready to provide you with the best boosting service and "
    #         "gaming experience in your favorite online games. We ensure that every customer is "
    #         "highly satisfied and 100% positive feedback of our work pretty much sums it up ;) Get "
    #         "the most relevant eu boost and power leveling.",
    #         "footer_description_uk": "Ми співпрацюємо лише з кваліфікованими та досвідченими провідними світовими гравцями, "
    #         "які особисто беруть участь у кожній події та готові надати вам найкращі послуги "
    #         "підвищення та ігровий досвід у ваших улюблених онлайн-іграх. Ми гарантуємо, "
    #         "що кожен клієнт буде дуже задоволений, і 100% позитивний відгук про нашу роботу майже "
    #         "підсумовує це ;) Отримайте найрелевантнішу підтримку та підвищення потужності для ЄС.",
    #         "header_top_text_en": "leave a trustpilot review and get an extra 10% off your next order!",
    #         "header_top_text_uk": "залиште відгук Trustpilot і отримайте додаткову знижку 10% на наступне замовлення!",
    #         "subscribe_form_text_en": "Sing up to our email newsteller and get 10% DISCOUNT on your first order!",
    #         "subscribe_form_text_uk": "Підпишіться на нашу електронну розсилку та отримайте ЗНИЖКУ 10% на перше "
    #         "замовлення!",
    #         "address1_link": "https://www.youtube.com/",
    #         "address2_link": "https://www.youtube.com/",
    #     }
    #     Setting.objects.create(**obj)
    #     for j in range(6):
    #         random_image = random.choice(os.listdir(os.path.join("seed", "insta_imgs")))
    #         image = open(os.path.join("seed", "insta_imgs", random_image), "rb")
    #         Insta.objects.create(
    #             img=File(image, "/media/" + image.name),
    #             img_alt_uk=self.fake_uk.word().capitalize(),
    #             img_alt_en=self.fake_en.word().capitalize(),
    #         )
    #     for j in range(20):
    #         Review.objects.create(
    #             author_en=self.fake_en.name(),
    #             author_uk=self.fake_uk.name(),
    #             source_of_review="dving.net",
    #             stars_count=self.fake_en.pyint(min_value=1, max_value=5),
    #             source_of_review_url="https://meet.google.com/",
    #             comment_en=self.fake_en.text(max_nb_chars=300),
    #             comment_uk=self.fake_uk.text(max_nb_chars=300),
    #         )
    #     for game in Game.objects.all():
    #         random_image = random.choice(os.listdir(os.path.join("seed", "news")))
    #         image = open(os.path.join("seed", "news", random_image), "rb")
    #         for i in range(6):
    #             News.objects.create(
    #                 title_en=self.fake_en.word().capitalize(),
    #                 title_uk=self.fake_uk.word().capitalize(),
    #                 description_en=self.fake_en.text(max_nb_chars=500),
    #                 description_uk=self.fake_uk.text(max_nb_chars=500),
    #                 image_alt_en=self.fake_en.word(),
    #                 image_alt_uk=self.fake_uk.word(),
    #                 game_id=game.id,
    #                 image=File(image, "/media/" + image.name),
    #             )
    #     for j in range(3):
    #         random_icon = random.choice(os.listdir(os.path.join("seed", "why_choose_us")))
    #         icon = open(os.path.join("seed", "why_choose_us", random_icon), "rb")
    #         WhyChooseUs.objects.create(
    #             title_en=self.fake_en.word().capitalize(),
    #             title_uk=self.fake_uk.word().capitalize(),
    #             description_en=self.fake_en.text(max_nb_chars=200),
    #             description_uk=self.fake_uk.text(max_nb_chars=200),
    #             icon=File(icon, "/media/" + icon.name),
    #             icon_alt_en=self.fake_en.word().capitalize(),
    #             icon_alt_uk=self.fake_uk.word().capitalize(),
    #         )
    #
    # def _create_tags(self):
    #     tags = [
    #         Tag(name_en="Hot", name_uk="Гаряче", color="#f63a3a"),
    #         Tag(name_en="New", name_uk="Новинка", color="#27ae60"),
    #         Tag(name_en="Limited", name_uk="Обмежено", color="#FFFFFF"),
    #     ]
    #     Tag.objects.bulk_create(tags)
    #
    # def _create_products(self):
    #     tags = Tag.objects.values_list("id", flat=True)
    #     for key, page in enumerate(CatalogPage.objects.all()):
    #         for i in range(1, 4):
    #             random_card_image = random.choice(os.listdir(os.path.join("seed", "card_image")))
    #             random_image = random.choice(os.listdir(os.path.join("seed", "banner")))
    #             card_image = open(os.path.join("seed", "card_image", random_card_image), "rb")
    #             image = open(os.path.join("seed", "banner", random_image), "rb")
    #             product = Product.objects.create(
    #                 title_en=f"Product {key}{i}",
    #                 title_uk=f"Продукт {key}{i}",
    #                 subtitle_en=self.fake_en.sentence(nb_words=3).capitalize(),
    #                 subtitle_uk=self.fake_uk.sentence(nb_words=3).capitalize(),
    #                 description_en=self.fake_en.text(max_nb_chars=600).capitalize(),
    #                 description_uk=self.fake_uk.text(max_nb_chars=600).capitalize(),
    #                 bonus_points=self.fake_en.pyint(min_value=10, max_value=150),
    #                 catalog_page_id=page.id,
    #                 sale_percent=0,
    #                 tag_id=random.choice(tags),
    #                 price_type="range" if i == 1 else "fixed",
    #                 price=self.fake_en.pyint(min_value=5, max_value=600),
    #                 image=File(image, "/media/" + image.name),
    #                 card_img=File(card_image, "/media/" + card_image.name),
    #                 card_img_alt_en=self.fake_en.word(),
    #                 card_img_alt_uk=self.fake_uk.word(),
    #                 image_alt_en=self.fake_en.word(),
    #                 image_alt_uk=self.fake_uk.word(),
    #             )
    #             product.save()
    #
    #             for j in range(4):
    #                 ProductTabs.objects.create(
    #                     title_en=self.fake_en.word().capitalize(),
    #                     title_uk=self.fake_uk.word().capitalize(),
    #                     content_en=self.fake_en.text(max_nb_chars=500).capitalize(),
    #                     content_uk=self.fake_uk.text(max_nb_chars=500).capitalize(),
    #                     product_id=product.id,
    #                     order=j,
    #                 )
    #     for prod in Product.objects.filter(price_type="range"):
    #         for j in range(4):
    #             filter_obj = Filter.objects.create(
    #                 title_en=self.fake_en.word().capitalize(),
    #                 title_uk=self.fake_uk.word().capitalize(),
    #                 type=random.choice(["Slider", "Radio", "CheckBox", "Select"]),
    #                 product_id=prod.id,
    #                 order=j,
    #             )
    #             for k in range(1, 5):
    #                 title_en = self.fake_en.word().capitalize()
    #                 title_uk = self.fake_uk.word().capitalize()
    #                 if filter_obj.type == "Slider":
    #                     title_en = k
    #                     title_uk = k
    #                 SubFilter.objects.create(
    #                     title_en=title_en,
    #                     title_uk=title_uk,
    #                     filter_id=filter_obj.id,
    #                     price=self.fake_en.pyint(min_value=5, max_value=100),
    #                     order=k,
    #                 )
    #     products_ids = Product.objects.filter(price_type="fixed").values_list("id", flat=True)
    #     for i in range(1, 4):
    #         freqbot = FreqBought.objects.create(
    #             title=f"Freqbot {i}",
    #             order=i,
    #             discount=self.fake_en.pyint(min_value=5, max_value=100),
    #         )
    #         for j in range(1, 4):
    #             freqbot.products.add(random.choice(products_ids))
