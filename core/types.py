import strawberry
from .models import *
# from django.auth.models import User
from django.contrib.auth.models import User
from typing import List, Optional
from strawberry import auto
# from django.contrib.auth.models import User

@strawberry.django.type(User,exclude=['password'])
class User:
    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    

@strawberry.django.type(Author,fields="__all__")
class Authors:
    user: User
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


@strawberry.django.type(Book,description="A book object query",fields="__all__")
class Books:
    author: Authors
    cover: str

    # @strawberry.field()
    # def cover(self,info) -> str:
    #     u