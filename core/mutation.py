import strawberry
import strawberry_django
from strawberry.field_extensions import InputMutationExtension
from .inputs import *
from .types import *
from .models import Author,Book
from graphql import GraphQLError
# @strawberry_django.mutation

from typing import Annotated, Union, List, Optional


# @strawberry.type
# class BookSuccess:
#     book: List[Book] = strawberry.field(resolver=Books)


# @strawberry.type
# class BookError:
#     username: str
#     alternative_username: str

# Response = Annotated[
#     Union[BookSuccess, BookError],
#     strawberry.union("BookResponse"),
# ]

# types=Union[Authors,Books]

@strawberry.type
class SuccessMessage:
    objects: Books 
    message: str

    def __init__(self, message: str, objects=None):
        self.message = message
        self.objects = objects 

@strawberry.type
class ErrorMessage:
    object:None
    field:str
    message: str


@strawberry.type
class BookMutation:
    @strawberry_django.mutation(name="Add_Books",description="Add book for author",handle_django_errors=True)
    def create_book(self, info, bookinput: BookInput) -> Union[SuccessMessage]:
        try:
            # print(dir(info.context.request.upload_handlers))
            # files=bookinput.cover.read().decode("utf-8")
            # print(files)
            aut=Author.objects.get(pk=bookinput.author).id
            book = Book.objects.create(author_id=aut,title=bookinput.title,description=bookinput.description,
                                       cover=bookinput.cover,price=bookinput.price,book_json=bookinput.book_json,
                                       time=bookinput.time,date=bookinput.date)
            return SuccessMessage(message="created",objects=book)
        except Author.DoesNotExist:
            raise GraphQLError("Author not found",path=['author'],extensions={'code':'AUTHOR_NOT_FOUND'},)
        except Exception as e:
            raise GraphQLError(str(e))
            # return ErrorMessage(field='author',message="Author not found",object=None)
                # return ErrorMessage(field='author',message="Author not found",object=None)
    @strawberry_django.mutation(name="update_Books",description="update book for author",handle_django_errors=True) 
    def update_book(self,info,id:strawberry.ID,bookinput:BookInput) -> Union[SuccessMessage]:
        try:
            books=Book.objects.get(pk=id)
            title=bookinput.title
            if title==strawberry.UNSET:
                title=books.title
            else:
                books.title=bookinput.title
            books.description=bookinput.description
            books.price=bookinput.price
            books.book_json=bookinput.book_json
            books.save()
            return SuccessMessage(message="updated",objects=books)
        except Book.DoesNotExist:
            raise GraphQLError("Book not found",path=['id'],extensions={"code":'BOOK NOT FOUND'})
        
    @strawberry_django.mutation(name="delete_Books",description="delete book for author",handle_django_errors=True)
    def delete_book(self,info,id:strawberry.ID) -> Union[SuccessMessage]:
        try:
            book=Book.objects.get(pk=id)
            book.delete()
            return SuccessMessage(message="deleted",objects=None)
        except Book.DoesNotExist:
            raise GraphQLError("Book not found",path=['id'],extensions={"code":'BOOK NOT FOUND'})


