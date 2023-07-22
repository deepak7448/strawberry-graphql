from django.contrib import admin
from .models import * 
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user','created_at','updated_at']
    search_fields = ['user__username','user__email']
    list_filter = ['created_at','updated_at']
    date_hierarchy = 'created_at'
    ordering = ['created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author','price','created_at','updated_at']
    search_fields = ['title','author__user__username','author__user__email']
    list_filter = ['created_at','updated_at']
    date_hierarchy = 'created_at'
    ordering = ['created_at']

