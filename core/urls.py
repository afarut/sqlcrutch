from django.urls import path
from core import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("user/insert/", views.user_insert, name="user_insert"),
    path("user/select/", views.user_select, name="user_select"),
    path("chapter/insert/", views.chapter_insert, name="chapter_insert"),
    path("chapter/select/", views.chapter_select, name="chapter_select"),
    path("book/insert/", views.book_insert, name="book_insert"),
    path("book/select/", views.book_select, name="book_select"),
    path("tag/insert/", views.tag_insert, name="tag_insert"),
    path("tag/select/", views.tag_select, name="tag_select"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)