import strawberry
from .models import *
# from django.auth.models import User
from django.contrib.auth.models import User
from typing import List, Optional
from strawberry import auto
from strawberry import relay
# from datetime import datetime
import datetime
# from django.contrib.auth.models import User

@strawberry.django.type(User,exclude=['password'])
class UserType(relay.Node):
    id: relay.NodeID[int]
    profile: 'ProfileType'
    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

@strawberry.django.type(Profile,fields="__all__")

class ProfileType(relay.Node):
    id: relay.NodeID[int]
    date_of_birth: auto
    address: auto
    user:UserType

@strawberry.django.filter(Author, lookups=True)
class AuthorFilter:
    name:auto
    user:auto

@strawberry.django.order(Author)
class AuthorOrder:
    id: auto
    name:auto
    user:auto

@strawberry.django.type(Author,fields="__all__",filters=AuthorFilter,order=AuthorOrder)
class Authors(relay.Node):
    id: relay.NodeID[int]
    user: UserType
    book: List['Books']
    profile_picture: str

    @strawberry.field
    def profile_picture(self,info) -> str:
        uri=info.context.request.build_absolute_uri()
        media=uri.replace('/graphql/','')
        url=media+self.profile_picture.url
        if self.profile_picture:
            return url
        return ''

@strawberry.django.filter(Book, lookups=True)
class BookFilter:
    author:auto
    title: auto
    date: Optional[datetime.date ]=strawberry.UNSET

@strawberry.django.type(Book,description="A book object query",fields="__all__",filters=BookFilter)
class Books(relay.Node):
    id: relay.NodeID[int]
    author: Authors
    cover: str

    # @strawberry.field(relay.Node[Book])
    # def node(self) -> Book:
    #     return self

@strawberry.django.type(Image,description="A image object query",fields="__all__")
class ImageType(relay.Node):
    id:relay.NodeID[int]
    image:str