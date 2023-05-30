from django.contrib import admin
from .models import Book, Genre, Tag, Chapter
# Register your models here.
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Chapter)