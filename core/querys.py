import strawberry
from .models import *
from .types import *
from typing import List, Optional, Union,Dict
from graphql import GraphQLError
from strawberry import relay

import strawberry_django





@strawberry.type
class BookQuery:
    @strawberry.field()
    def books_id(self, id: int,) -> List[Books]:
        try:
            book = Book.objects.get(pk=id)
            return [book]
        except:
            # raise GraphQLError('Book not found')   
             raise GraphQLError("Book not found",path=['book'],extensions={'code':'BOOK_NOT_FOUND'})
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


@strawberry.type
class BookRealyQuery:
    book: relay.Node = relay.node()
    # books: relay.ConnectionField[Books] = relay.connection_field(Books)
    @strawberry.django.connection(relay.ListConnection[Books])
    def book_relay(self,info,)->List[Books]:
        book=Book.objects.all()
        # if filters is not strawberry.UNSET:
            # book=strawberry_django.filters.apply(filters,book,info)
        return book
    
# @strawberry.django.filter(Author,)
# class AuthorFilter:
#     name:auto
#     user:auto

@strawberry.type
class AuthorRealyQuery:
    author: relay.Node = relay.node()

    @strawberry.django.connection(relay.ListConnection[Authors])
    def author_relay(self,info,
                    # filters:AuthorFilter|None=strawberry.UNSET,
                    )->List[Authors]:
        autor=Author.objects.all()
        # if filters is not strawberry.UNSET:
        #     autor=strawberry_django.filters.apply(filters,autor,info)
        return autor