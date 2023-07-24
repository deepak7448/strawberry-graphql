import strawberry
from strawberry_django.optimizer import DjangoOptimizerExtension

from .types import Book
# from .query import books_all
from typing import List, Optional, Union

from .querys import BookQuery,BookRealyQuery,AuthorRealyQuery
from .mutation import *
from strawberry_django_jwt.middleware import JSONWebTokenMiddleware
# from strawberry_jwt_auth.extension import JWTExtension
# import graphql_jwt
import strawberry_django_jwt.mutations as jwt_mutations
# from gqlauth.user import relay as mutations
# from gqlauth.user import arg_mutations as mutations

@strawberry.type
class Query(BookRealyQuery,AuthorRealyQuery):
    pass

@strawberry.type
class Mutation(BookMutation,RegisterUserMutation,LoginMutation):
    token_auth = jwt_mutations.ObtainJSONWebToken.obtain
    verify_token = jwt_mutations.Verify.verify
    refresh_token = jwt_mutations.Refresh.refresh
    pass
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
        JSONWebTokenMiddleware,
    ],
)