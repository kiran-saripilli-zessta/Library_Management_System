from django import forms 
from .models import BookModel, UserProfile

class BookForm(forms.ModelForm):
    class Meta:
        model =  BookModel
        fields = ['book_title','book_author','book_genre','book_unique_isbn','book_publisher']