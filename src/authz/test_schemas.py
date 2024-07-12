from ninja import ModelSchema

from src.users.models import User


class UserTestOutSchema(ModelSchema):
    """
    Pydantic schema for User.

    Purpose of this schema to return user's
    personal data
    """
    date_joined: str
    birthday: str

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "nickname",
            "date_joined",
            "city",
            "man",
            "phone_number",
            "email",
            "address",
            "is_superuser",
            "birthday", ]