import strawberry
from strawberry import auto
from .models import Book, Author, User
from .types import *
from typing import Optional
from strawberry.file_uploads import Upload
# from graphene_file_upload.scalars import Upload
# from strawberry.types import GenericScalar

@strawberry.django.input(Book)
class BookInput:
    # id: auto
    author:strawberry.ID
    title: Optional[str]=strawberry.UNSET
    description: auto
    book_json:auto
    cover: Upload
    price: auto 
    time:auto
    date:auto
# class FruitInput:
#     id: auto
#     name: auto
#     color: "ColorInput"