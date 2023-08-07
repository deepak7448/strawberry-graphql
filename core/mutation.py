import strawberry
import strawberry_django
from strawberry.field_extensions import InputMutationExtension
from .inputs import *
from .types import *
from .models import Author,Book
from graphql import GraphQLError
from strawberry.scalars import JSON
from typing import Annotated, Union, List, Optional,Dict
from strawberry.types import Info
from strawberry_django_jwt.shortcuts import get_token,create_refresh_token
from strawberry_django_jwt.refresh_token.models import RefreshToken
from strawberry_django_jwt.decorators import login_required
from graphql_relay import to_global_id, from_global_id
from .utils import login
# from strawberry_django_jwt.decorators import login_field

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

types=Union[Authors,Books,UserType,ProfileType]

@strawberry.type
class SuccessMessage:
    message: str
    objects: types
    

    def __init__(self, message: str, objects=None):
        self.message = message
        self.objects = objects 



@strawberry.type
class ErrorMessage:
    message: str
    errors: List[JSON]

    # def __init__(self, message: str, objects=None,errors=None):
    #     self.message = message
    #     self.objects = objects 
    #     self.errors=errors

@strawberry.type
class BookMutation:
    @strawberry.mutation(name="Add_Books",description="Add book for author")
    @login_required
    def create_book(self, info, bookinput: BookInput) -> Union[SuccessMessage,ErrorMessage]:
        try:
            errors=[]
            file=info.context.request.FILES
            if len(file)==0:
                i=None
            else:
                for i in file.values():
                    i=i
            if bookinput.time==strawberry.UNSET or time==None or time=="":
                bookinput.time=None
            if bookinput.date==strawberry.UNSET or date==None or date=="":
                bookinput.date=None
            if bookinput.book_json==strawberry.UNSET or bookinput.book_json=="" or bookinput.book_json==None:
                bookinput.book_json=None
            aut=Author.objects.get(pk=bookinput.author).id
            book = Book.objects.create(author_id=aut,title=bookinput.title,description=bookinput.description,
                                       price=bookinput.price,book_json=bookinput.book_json,cover=i,
                                       time=bookinput.time,date=bookinput.date)
            return SuccessMessage(message="created",objects=book)
        except Author.DoesNotExist:
            errors.append({'message':"Author not found","field":"author"})
            return ErrorMessage(errors=errors,message="error")
            # raise GraphQLError("Author not found",path=['author'],extensions={"code":'AUTHOR NOT FOUND'})
        except Exception as e:
            raise GraphQLError(str(e))
            # return ErrorMessage(field='author',message="Author not found",object=None)
                # return ErrorMessage(field='author',message="Author not found",object=None)
    @strawberry_django.mutation(name="update_Books",description="update book for author",handle_django_errors=True) 
    @login_required
    def update_book(self,info,id:strawberry.ID,bookinput:BookInput) -> Union[SuccessMessage,]:
        try:
            id=from_global_id(id).id
            books=Book.objects.get(pk=id)
            if books.title==strawberry.UNSET:
                books.title=None
            elif bookinput.price==strawberry.UNSET:
                bookinput.price=None
            elif bookinput.description==strawberry.UNSET:
                bookinput.description=None
            elif bookinput.book_json==strawberry.UNSET:
                bookinput.book_json=None
            books.title=bookinput.title
            books.description=bookinput.description
            books.price=bookinput.price
            books.book_json=bookinput.book_json
            books.save()
            return SuccessMessage(message="updated",objects=books)
        except Book.DoesNotExist:
            raise GraphQLError("Book not found",path=['id'],extensions={"code":'BOOK NOT FOUND'})
        
    @strawberry_django.mutation(name="delete_Books",description="delete book for author",handle_django_errors=True)
    @login_required
    def delete_book(self,info,id:strawberry.ID) -> Union[SuccessMessage]:
        try:
            book=Book.objects.get(pk=id)
            book.delete()
            return SuccessMessage(message="deleted",objects=None)
        except Book.DoesNotExist:
            raise GraphQLError("Book not found",path=['id'],extensions={"code":'BOOK NOT FOUND'})

@strawberry.type
class RegisterMessage:
    message: str
    objects: UserType
    token:str
    refresh_token:str
    

@strawberry.type
class RegisterUserMutation:
    @strawberry_django.mutation(name="Register_User",description="Register user",handle_django_errors=True)
    def register_user(self,info,userinput:UserInput,) -> Union[ErrorMessage,RegisterMessage]:
        try:
            errors=[]
            email=User.objects.filter(email=userinput.email)
            username=User.objects.filter(username=userinput.username)
            if email.exists():
                errors.append({'message':"Email already exists","field":"email"})
            if username.exists():
                errors.append({'message':"Username already exists","field":"username"})
            if userinput.password!=userinput.confirm_password:
                errors.append({'message':"Password and conform password not match","field":"password"})
            if errors:
                return ErrorMessage(errors=errors,message="error")
            if userinput.profile.date_of_birth is None or userinput.profile.date_of_birth=="":
                userinput.profile.date_of_birth=None
            user=User.objects.create(username=userinput.username,email=userinput.email,
                                          first_name=userinput.first_name,last_name=userinput.last_name)
            user.set_password(userinput.password)
            user.save()
            ref=create_refresh_token(user)
            tok=get_token(user)
            profile=Profile.objects.create(user=user,date_of_birth=userinput.profile.date_of_birth,address=userinput.profile.address)

            return RegisterMessage(message="created",objects=user,token=tok,refresh_token=ref)
        except Exception as e:
            raise GraphQLError(str(e))
        
@strawberry.type
class LoginMessage:
    objects: UserType
    message:str
    token:str
    refresh_token:str

@strawberry.type
class LoginMutation:
    @strawberry_django.mutation(name="Login_User",description="Login user",handle_django_errors=True)
    def UserLogin(self,info,logininput:UserLoginInput,) -> Union[ErrorMessage,LoginMessage]:
        try:
            username=logininput.username
            password=logininput.password
            user_login=login(User,username,password)
            # user=[item for item in user_login if "field" in item]
            # print(user_login)
            for user in user_login:
                if "field" in user:
                    return ErrorMessage(errors=user_login,message="error")
                else:
                    ref=create_refresh_token(user['user'])
                    tok=get_token(user['user'])
                    re_token=RefreshToken.objects.filter(user=user['user'])
                    for i in re_token:
                        token=i.is_expired()
                        if token:
                            i.delete()
                        # else:
                        #     print(token)
                        #     pass
                            # i.delete()
                            # refesh_token.append(i.token)

                    return LoginMessage(message="Login successfull",objects=user['user'],token=tok,refresh_token=ref)
        except Exception as e:
            raise GraphQLError(str(e))
        

@strawberry.type
class ImageUpload:
    @strawberry_django.mutation(name="Upload_Image",description="Upload image",handle_django_errors=True)
    def uploadImgae(self,info,image:ImageInput)-> ImageType:
        # print(img)
        for i in image:
            print(i)
        # contents = []
        # for file in img:
        #     content = file.read().decode("utf-8")
        #     contents.append(content)
        return "img"
        # try:
        #     for i in img:
        #         Image.objects.create(image=i.image)
        #     return ImageType.objects.all()
        # except Exception as e:
        #     raise GraphQLError(str(e))


@strawberry.type
class BulkDataMessage:
    message: str
    # objects: List[Books]

@strawberry.type
class Bulkdata:
    @strawberry_django.mutation(name="Bulk_Data",description="Bulk data",handle_django_errors=True)
    def bulkdata(self,info,booksinput:List[BookInput])-> Union[BulkDataMessage,ErrorMessage]:
        try:
            errors=[]
            bulk_data=[]
            for data in booksinput:
                print(data)
            return BulkDataMessage(message="created")
        except Exception as e:
            errors.append({'message':str(e),"field":"error"})
            return ErrorMessage(errors=errors,message="error")

