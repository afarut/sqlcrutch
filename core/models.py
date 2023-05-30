from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .utils import slugify
from django.conf import settings


class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    views = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=settings.IMAGE_FOLDER)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")
    tags = models.ManyToManyField("Tag", blank=True, related_name="books")
    genres = models.ManyToManyField("Genre", blank=True, related_name="books")

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    num = models.FloatField()
    title = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.book.title}:{self.title}"


class Tag(models.Model):    
    title = models.CharField(max_length=60)     
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Genre(models.Model):    
    title = models.CharField(max_length=60)     
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'