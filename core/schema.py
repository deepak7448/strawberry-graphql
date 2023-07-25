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
from strawberry.file_uploads import Upload

@strawberry.type
class Query(BookRealyQuery,AuthorRealyQuery):
    pass

@strawberry.type
class Mutation(BookMutation,RegisterUserMutation,LoginMutation):
    token_auth = jwt_mutations.ObtainJSONWebToken.obtain
    verify_token = jwt_mutations.Verify.verify
    refresh_token = jwt_mutations.Refresh.refresh

    # @strawberry.mutation
    # def read_file(self, info,file: Upload) -> str:
    #     file=info.context.request.FILES
    #     for i in file.values():
    #         print(i)
    #     print(file)
    #     # print(file.read().decode("utf-8"))
    #     return "trye"
    pass
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
        JSONWebTokenMiddleware,
    ],
)


# { "query": "mutation($file: Upload!){ readFile(file: $file) }", "variables": { "file": null } }
# {"query":"mutation($cover: Upload!){Add_Books(bookinput:{author: 2,cover: $cover,description:"",price:10,title:""}){... on SuccessMessage { message }}}","variables": { "cover": null }}


# {"query":"mutation($cover: Upload!,$title:String){Add_Books(bookinput:{author: 2,cover: $cover,price:10,title:$title}){... on SuccessMessage { message }}}","variables": { "cover": null,"title":null}}