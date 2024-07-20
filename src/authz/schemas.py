from ninja_jwt.schema import TokenObtainPairOutputSchema
from ninja_jwt.schema_control import SchemaControl
from ninja_jwt.settings import api_settings
from pydantic.networks import EmailStr

from src.users.models import User

schema = SchemaControl(api_settings)


class LoginSchema(schema.obtain_pair_schema):
    """Pydantic schema for return message to client side.

    Purpose of this schema just say that operation
    has been successful or failed
    """

    email: EmailStr
    password: str


class LoginResponseSchema(schema.obtain_pair_schema.get_response_schema()):
    """Pydantic schema for return message to client side.

    Purpose of this schema just say that operation
    has been successful or failed
    """

    admin: bool

    @staticmethod
    def resolve_admin(obj: TokenObtainPairOutputSchema):
        user_email = obj.dict()["email"]
        user = User.objects.get(email=user_email)
        return user.is_superuser
