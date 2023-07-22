import strawberry
from .models import *
from .types import *
from typing import List, Optional, Union,Dict
from graphql import GraphQLError

import strawberry_django

@strawberry.django.filter(Book, lookups=True)
class BookFilter:
    id: auto
    author:auto
    title: auto


@strawberry.django.order(Book)
class BookOrder:
    id: auto
    author:auto
    title: auto


@strawberry.django.type(Book, order=BookOrder)
class BookOR:
    id: auto
    title: auto

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
        

    # @strawberry.field
    @strawberry.django.field
    def book_all(self,info,
                filters:BookFilter|None=strawberry.UNSET,
                # order:BookOrder|None=strawberry.UNSET,
               )->List[Books]:
        book=Book.objects.all()
        if filters is not strawberry.UNSET:
            book=strawberry_django.filters.apply(filters,book,info)
        # if order is not strawberry.UNSET:
        #     if order.id is not None:
        #         book = book.order_by(order.id)
        #     if order.author is not None:
        #         book = book.order_by(order.author)
        #     if order.title is not None:
        #         book = book.order_by(order.title)
        return book
    # bookoe: List[Books] = strawberry.django.field(order=BookOrder)
    # fruits: list[Books] = strawberry.django.field()
    # authors: list[Authors] = strawberry.django.field()