from django.shortcuts import render, redirect
from .forms import BookForm, RegForm, ChapterForm
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.contrib.auth.hashers import make_password
from .utils import slugify, get_tags, get_genres, generate, image_save, get_users, get_books, get_chapters
from django.conf import settings

def index(request):
    return render(request, "core/base.html")


@csrf_exempt
def user_insert(request):
    if request.method == "POST":
        if request.POST.get("password2") != request.POST.get("password1"):
            raise Exception("Password fields are not equal")
        with connections.create_connection("default").cursor() as cursor:
            cursor.execute("""
                INSERT INTO auth_user (is_superuser, is_staff, is_active, date_joined, username, email, first_name, password, last_name)
                VALUES (false, false, false, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s)
            """, [request.POST.get("username"), request.POST.get("email"), request.POST.get("first_name"), make_password(request.POST.get("password2")), request.POST.get("last_name")])
    return render(request, "core/user_insert.html", {"form": RegForm()})


def user_select(request):
    users = get_users()
    return render(request, "core/user_select.html", {"users": users})


@csrf_exempt
def chapter_insert(request):
    books = get_books()
    if request.method == "POST":
        with connections.create_connection("default").cursor() as cursor:
            if not request.POST.get("num"):
                num = 0
            else:
                num = request.POST.get("num")
            cursor.execute("""
                INSERT INTO core_chapter (title, num, text, pub_date, book_id)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s)
            """, [request.POST.get("title"), num, request.POST.get("text"), request.POST.get("book")])
    return render(request, "core/chapter_insert.html", {"books": books})


def chapter_select(request):
    chapters = get_chapters()
    return render(request, "core/chapter_select.html", {"chapters": chapters})


@csrf_exempt
def book_insert(request):
    tags = get_tags()
    genres = get_genres()
    users = get_users()
    if request.method == "POST":
        image = image_save(request.FILES["image"])
        title = request.POST.get("title")
        description = request.POST.get("description")
        tag_ids = request.POST.getlist("tags")
        genre_ids = request.POST.getlist("genres")
        author_id = request.POST.get("author")
        with connections.create_connection("default").cursor() as cursor:
            cursor.execute("""
                INSERT INTO core_book (title, description, author_id, image, views, pub_date)
                VALUES (%s, %s, %s, %s, 0, CURRENT_TIMESTAMP)
            """, [title, description, author_id, image])
            cursor.execute("SELECT id FROM core_book WHERE title = %s", [title,])
            book_id = cursor.fetchone()[0]
            for genre_id in genre_ids:
                cursor.execute("""
                    INSERT INTO core_book_genres (book_id, genre_id)
                    VALUES (%s, %s)
                """, [book_id, genre_id])
            for tag_id in tag_ids:
                cursor.execute("""
                    INSERT INTO core_book_tags (book_id, tag_id)
                    VALUES (%s, %s)
                """, [book_id, tag_id])
    return render(request, "core/book_insert.html", {"genres": genres, "tags": tags, "users": users})


def book_select(request):
    books = get_books()
    return render(request, "core/book_select.html", {"books": books})


@csrf_exempt
def tag_insert(request):
    if request.method == "POST":
        with connections.create_connection("default").cursor() as cursor:
            if not request.POST.get("slug"):
                slug = slugify(request.POST.get("title"))
            else:
                slug = request.POST.get("slug")
            cursor.execute("""
                INSERT INTO core_tag (title, slug)
                VALUES (%s, %s)
            """, [request.POST.get("title").lower(), slug])
    return render(request, "core/tag_insert.html")


def tag_select(request):
    tags = get_tags()
    return render(request, "core/tag_select.html", {"tags": tags})


def get_books_by_genre(request, slug):
    data = get_books()
    books = []
    for book in data:
        for genre in book["genres"]:
            if genre["slug"] == slug:
                books.append(book)
                break
    return render(request, "core/book_select.html", {"books": books})


def get_books_by_tag(request, slug):
    data = get_books()
    books = []
    for book in data:
        for tag in book["tags"]:
            if tag["slug"] == slug:
                books.append(book)
                break
    return render(request, "core/book_select.html", {"books": books})


def get_book_by_id(request, book_id):
    books = get_books(f"WHERE core_book.id={book_id}")
    return render(request, "core/book_select.html", {"books": books})


def get_chapter_by_id(request, chapter_id):
    chapters = get_chapters(f"WHERE id={chapter_id}")
    return render(request, "core/chapter_select.html", {"chapters": chapters})


def get_user_by_id(request, user_id):
    users = get_users(f"WHERE id = {user_id}")
    return render(request, "core/user_select.html", {"users": users})