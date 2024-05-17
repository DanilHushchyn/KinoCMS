from django.db import models


# Create your models here.
class MovieTech(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "MovieTech"
        verbose_name_plural = "MovieTechs"
        db_table = 'movie_techs'


class MovieGenre(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "MovieGenre"
        verbose_name_plural = "MovieGenres"
        db_table = 'movie_genres'


class MovieParticipantPerson(models.Model):
    fullname = models.CharField(max_length=255)

    class Meta:
        verbose_name = "MovieParticipant"
        verbose_name_plural = "MovieParticipants"
        db_table = 'movie_participant_persons'


class MovieParticipantRole(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "MovieParticipantRole"
        verbose_name_plural = "MovieParticipantRoles"
        db_table = 'movie_participant_roles'


class MovieParticipant(models.Model):
    person = models.ForeignKey(MovieParticipantPerson,
                               on_delete=models.CASCADE, null=True)
    role = models.ForeignKey(MovieParticipantRole,
                             on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "MovieParticipant"
        verbose_name_plural = "MovieParticipants"
        db_table = 'movie_participants'


class Movie(models.Model):
    slug = models.SlugField(db_index=True, unique=True, null=True)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=2000)
    banner = models.ForeignKey('core.Image',
                               related_name='movie_bnr',
                               on_delete=models.CASCADE,
                               null=True, parent_link=True)
    card_img = models.ForeignKey('core.Image',
                                 related_name='movie_card',
                                 on_delete=models.CASCADE,
                                 null=True, parent_link=True)
    trailer_link = models.URLField(null=True)
    year = models.PositiveIntegerField(null=True)
    budget = models.PositiveIntegerField(null=True)
    legal_age = models.PositiveIntegerField(null=True)
    duration = models.DurationField(null=True)
    techs = models.ManyToManyField('MovieTech')
    genres = models.ManyToManyField('MovieGenre')
    released = models.DateField()
    participants = models.ManyToManyField('MovieParticipant')
    # countries = models.CharField(max_length=255, null=True)
    seo = models.OneToOneField('core.Seo', on_delete=models.CASCADE,
                               parent_link=True, null=True)
    gallery = models.OneToOneField('core.Gallery',
                                   on_delete=models.CASCADE,
                                   null=True)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        db_table = 'movies'
