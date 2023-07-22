import strawberry
from .models import *
from .types import *
from typing import List, Optional, Union,Dict
from graphql import GraphQLError


@strawberry.type
class BookQuery:
    @strawberry.field()
    def books_by_id(self, id: int,) -> List[Books]:
        try:
            book = Book.objects.get(pk=id)
            return [book]
        except:
            # raise GraphQLError('Book not found')   
             raise GraphQLError("Book not found",path=['book'],extensions={'code':'BOOK_NOT_FOUND'})
        

    @strawberry.field
    def book_all(self,info)->List[Books]:
        book=Book.objects.all()
        return book
    # fruits: list[Books] = strawberry.django.field()
    # authors: list[Authors] = strawberry.django.field()