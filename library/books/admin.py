from django.contrib import admin
from .models import Author, Book, Bookinstance, Genre


# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Bookinstance)
admin.site.register(Genre)
