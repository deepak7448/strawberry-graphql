import strawberry
from strawberry import auto
from .models import Book, Author, Profile
from .types import *
from typing import Optional
from strawberry.file_uploads import Upload
from django.contrib.auth.models import User
import datetime
from typing import NewType

# from graphene_file_upload.scalars import Upload
# from strawberry.types import GenericScalar

@strawberry.django.input(Book)
class BookInput:
    # id: auto
    author:strawberry.ID
    title: Optional[str]=strawberry.UNSET
    description: Optional[str]=strawberry.UNSET
    book_json:auto
    cover: Upload
    price: Optional[int]=strawberry.UNSET 
    time:auto
    date:auto
# class FruitInput:
#     id: auto
#     name: auto
#     color: "ColorInput"

@strawberry.django.input(Profile)
class ProfileInput:
    # id: auto
    # user:strawberry.ID
    date_of_birth:Optional[str]=strawberry.UNSET
    address: auto

#for additional field in input
#using class and lambda
@strawberry.scalar
class DateOfBirth:
    def __init__(self, default_date: str = None):
        self.default_date = default_date

    @staticmethod
    def serialize(value: datetime.date) -> str:
        return value.isoformat()

    @staticmethod
    def parse_value(value: str) -> datetime.date:
        return datetime.date.fromisoformat(value)

    @staticmethod
    def parse_literal(node) -> datetime.date:
        if isinstance(node, str):
            return datetime.date.fromisoformat(node.value)
        return None



date_of_birth = strawberry.scalar(
    NewType("date_of_birth", str),
    serialize=lambda v: v.isoformat(),
    parse_value=lambda v:datetime.date.fromisoformat(v),) 

confirm_password = strawberry.scalar(
    NewType("confirm_password", str),
    serialize=lambda v: v,
    parse_value=lambda v:v,) 

@strawberry.django.input(User)
class UserInput:
    # id: auto
    username:auto
    email: auto
    password: auto
    confirm_password:confirm_password
    first_name: auto
    last_name: auto
    profile: ProfileInput
    # date_of: date_of_birth
    # address: auto

@strawberry.django.input(User)
class UserLoginInput:
    username:auto
    password: auto