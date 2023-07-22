import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from .types import Book
# from .query import books_all
from typing import List, Optional, Union

from .querys import BookQuery 
from .mutation import BookMutation

@strawberry.type
class Query(BookQuery):
    pass

@strawberry.type
class Mutation(BookMutation):
    pass
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)