from strawberry.django.views import GraphQLView
# from strawberry_jwt_auth.views import strawberry_auth_view
# from .schema import schema
# from django.urls import path
# urlpatterns = [
#     path("graphql", GraphQLView.as_view(schema=schema)),
# ]


from django.urls import include, path
from strawberry.django.views import AsyncGraphQLView

from .schema import schema

urlpatterns = [
    path('graphql/', GraphQLView.as_view(schema=schema)),
]