import strawberry
from .models import *
from .types import *
from typing import List, Optional, Union,Dict
from graphql import GraphQLError
from strawberry import relay
import strawberry_django
from strawberry_django_jwt.decorators import login_required
# from graphql_relay import to_global_id, from_global_id
from .utils import deocodeGlobalId



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
    book: Books = relay.node()

    @strawberry.django.field()
    @login_required
    def book(self,info,id:relay.GlobalID)->List[Books]:
        id=deocodeGlobalId(id)
        return Book.objects.get(pk=id)

    # books: relay.ConnectionField[Books] = relay.connection_field(Books)
    @strawberry.django.connection(relay.ListConnection[Books])
    @login_required
    def book_relay(self,info,)->List[Books]:
        book=Book.objects.all()
        # if filters is not strawberry.UNSET:
            # book=strawberry_django.filters.apply(filters,book,info)
        return book
    
# @strawberry.django.filter(Author,)
# class AuthorFilter:
#     name:auto
#     user:auto
# @login_required
@strawberry.type
class AuthorRealyQuery:
    author: Authors = relay.node()
    @strawberry.django.field()
    def resolve_author(self,info,id:relay.NodeID[int])->List[Authors]:
        return Author.objects.get(pk=id)


    @strawberry.django.connection(relay.ListConnection[Authors])
    def author_relay(self,info,
                    # filters:AuthorFilter|None=strawberry.UNSET,
                    )->List[Authors]:
        autor=Author.objects.all()
        # if filters is not strawberry.UNSET:
        #     autor=strawberry_django.filters.apply(filters,autor,info)
        return autor