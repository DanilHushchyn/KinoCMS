from datetime import datetime, timedelta
from os.path import splitext

from django.core.paginator import EmptyPage, Paginator

from ninja.errors import HttpError
from django.db.models import QuerySet

from src.users.models import User


def get_timestamp_path(instance: object, filename) -> str:
    """
    Make unique naming of files in directory media.

    :param instance: model instance which just created
    :param filename: name of uploaded file to ImageField
    :return: unique file name
    """

    return "%s%s" % (
        datetime.now().timestamp(),
        splitext(filename)[1],
    )


def paginate(page: int, items: QuerySet, page_size: int) -> dict:
    """
    Returns paginated queryset by pages of any Model in our project.

    :param page: the page number we want to get
    :param items: queryset of models instances which have to paginated
    :param page_size: length of queryset per page
    :return: dict which contains parameters for pagination
    :rtype: dict
    """
    if page_size < 1:
        raise HttpError(422, "page_size query parameter must be more than 1")
    paginator = Paginator(items, per_page=page_size)
    try:
        paginated_items = paginator.page(page)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    return {
        "items": paginated_items.object_list,
        "count": paginator.num_pages,
        "next": paginated_items.has_next(),
        "previous": paginated_items.has_previous(),
    }



