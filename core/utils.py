from django.template.defaultfilters import slugify as django_slugify
from core.constants import ALPHABET
from django.db import connections
import string
import random
from django.conf import settings


def slugify(s):
    return django_slugify("".join(ALPHABET.get(w, w) for w in s.lower()))


def get_tags():
    with connections.create_connection("default").cursor() as cursor:
        cursor.execute("""
            SELECT id, title, slug FROM core_tag
        """)
        rows = cursor.fetchall()
        tags = []
        for row in rows:
            data = {"id": row[0], "title": row[1], "slug": row[2]}
            tags.append(data)
        return tags
    return []


def get_genres():
    with connections.create_connection("default").cursor() as cursor:
        cursor.execute("""
            SELECT id, title, slug FROM core_genre
        """)
        rows = cursor.fetchall()
        genres = []
        for row in rows:
            data = {"id": row[0], "title": row[1], "slug": row[2]}
            genres.append(data)
        return genres
    return []


def generate(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def image_save(file):
    last_name = file.name.split(".")
    name = f"{last_name[0]}{generate()}.{last_name[1]}"
    with open(f"media/{settings.IMAGE_FOLDER}{name}", 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return settings.IMAGE_FOLDER + name


def get_users(conditions=""):
    users = []
    with connections.create_connection("default").cursor() as cursor:
        cursor.execute(f"""
            SELECT username, email, first_name, id, last_name FROM auth_user {conditions}
        """)
        rows = cursor.fetchall()
        for row in rows:
            data = {"username": row[0], "email": row[1], "first_name": row[2] if row[2] else None, "id": row[3], "last_name": row[4] if row[4] else None}
            users.append(data)
    return users


def get_books(conditions=""):
    books = []
    with connections.create_connection("default").cursor() as cursor:
        cursor.execute(f"SELECT core_book.id, core_book.title, core_book.description, views, pub_date, author_id, image, auth_user.username FROM core_book JOIN auth_user ON auth_user.id = core_book.author_id {conditions}")
        for book in cursor.fetchall():
            data = {"id": book[0], "title": book[1], "description": book[2], "views": book[3], "pub_date": book[4], "author_id": book[5], "image": settings.MEDIA_URL+book[6], "author_username": book[7]}
            cursor.execute("SELECT title, slug FROM core_tag JOIN core_book_tags ON core_tag.id=core_book_tags.tag_id WHERE core_book_tags.book_id = %s", [book[0], ])
            data["tags"] = []
            for tag in cursor.fetchall():
                data["tags"].append({"title": tag[0], "slug": tag[1]})
            cursor.execute("SELECT title, slug FROM core_genre JOIN core_book_genres ON core_genre.id=core_book_genres.genre_id WHERE core_book_genres.book_id = %s", [book[0], ])
            data["genres"] = []
            for genre in cursor.fetchall():
                data["genres"].append({"title": genre[0], "slug": genre[1]})
            books.append(data)
    return books


def get_chapters(conditions=""):
    chapters = []
    with connections.create_connection("default").cursor() as cursor:
        cursor.execute(f"SELECT id, num, title, text, pub_date, book_id FROM core_chapter {conditions}")
        for chapter in cursor.fetchall():
            data = {"id": chapter[0], "num": chapter[1], "title": chapter[2], "text": chapter[3], "pub_date": chapter[4], "book_id": chapter[5]}
            chapters.append(data)
    return chapters