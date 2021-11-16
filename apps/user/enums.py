from utils.graphene.enums import (
    convert_enum_to_graphene_enum,
    get_enum_name_from_django_field,
)

from .models import User

UserGenderEnum = convert_enum_to_graphene_enum(User.Gender, name='UserGenderEnum')

enum_map = {
    get_enum_name_from_django_field(field): enum
    for field, enum in (
        (User.gender, UserGenderEnum),
    )
}
