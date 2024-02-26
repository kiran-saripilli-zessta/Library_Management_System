import uuid
from rest_framework import serializers
from .models import *



class AuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class BookModelSerializer(serializers.ModelSerializer):

    book_author = AuthorModelSerializer(many=False)
    book_genre = GenreSerializer()
    class Meta:
        model = BookModel
        fields = ['book_title', 'book_author', 'book_genre', 'book_unique_isbn', 'book_publisher', 'quantity_available']

    def get_auto_generated_isbn(self, obj):
        if not obj.book_unique_isbn:
            unique_identifier = uuid.uuid4().hex[:12].upper()
            obj.book_unique_isbn = f'ISBN-{unique_identifier}'
            obj.save()  # Save the object to persist the generated ISBN

        return obj.book_unique_isbn


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class LoanModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanModel
        fields = '__all__'

class MemberModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberModel
        fields = '__all__'
