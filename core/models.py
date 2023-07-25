from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='author')
    name=models.CharField(max_length=100,null=True,blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Authors"


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE,related_name='book')
    book_json=models.JSONField(null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    slug=models.SlugField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    time=models.TimeField(null=True,blank=True)
    date=models.DateField(null=True,blank=True)
    cover = models.ImageField(upload_to='covers/',null=True,blank=True)
    price = models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if self.slug=='' or self.slug==None:
            self.slug=slugify(self.title,allow_unicode=True)
        super(Book,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = "Books"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    date_of_birth=models.DateField(null=True,blank=True)
    address=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Profiles"


class Image(models.Model):
    image=models.ImageField(upload_to='images/',null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.url
    
    class Meta:
        verbose_name_plural = "Images"