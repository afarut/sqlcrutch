from django import forms
from .models import Book, Tag, Chapter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'description', 'image', 'tags', 'genres', "author"]


class RegForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='')
	username = forms.CharField(max_length = 100, help_text='')
	password1 = forms.CharField(max_length = 100, help_text='')
	password2 = forms.CharField(max_length = 100, help_text='')
	first_name = forms.CharField(max_length = 100, help_text='')

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'password1', 'password2', ]


class ChapterForm(forms.ModelForm):
	class Meta:
		model = Chapter
		fields = ["book", "num", "title", "text"]