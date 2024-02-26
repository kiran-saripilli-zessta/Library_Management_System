from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from storages.backends.s3boto3 import S3Boto3Storage


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name



class Genre(models.Model):
    genre_name = models.CharField(max_length=200, unique=False, null=True)

    def get_genre(self):
        return self.genre_name

    def __str__(self):
        return self.genre_name
    
class DemoModel(models.Model):
    demo_name = models.CharField(max_length=200)

    def __str__(self):
        return self.demo_name

class BookModel(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.ForeignKey('Author', on_delete=models.CASCADE,related_name='author', blank=True)
    book_genre = models.ForeignKey('Genre', on_delete=models.CASCADE ,related_name='genre',blank=True)
    book_unique_isbn = models.CharField(max_length=20, unique=True)
    quantity_available = models.PositiveIntegerField(default=0)
    book_publisher = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.book_title

    @property
    def is_available(self):
        return self.quantity_available > 0
    


class MemberModel(models.Model):
    member_name = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    member_books_borrowed = models.ManyToManyField('BookModel', related_name='borrowers', blank=True)

    def __str__(self):
        return self.member_name.username
    

class LoanModel(models.Model):
    member = models.ForeignKey('MemberModel', on_delete=models.CASCADE, related_name='loans')
    book = models.ForeignKey('BookModel', on_delete=models.CASCADE, related_name='loans')
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    loan_status = models.CharField(max_length=20)  #  'On Loan', 'Returned', 'Overdue'
    loan_date = models.DateField(auto_now_add=True) 

    def __str__(self):
        return f"{self.member.member_name.username} - {self.book.book_title}"

    def get_notification_data(self):
        return {
            'due_date': self.due_date,
            'fine': self.fine,
            'member_name': self.member.member_name.username,
            'book_name': self.book.book_title,
        }
    


class S3MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False


    
class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user_photo = models.ImageField(upload_to='media',storage=S3MediaStorage())




    def __str__(self):
        return self.username

    def get_user_photo_url(self):
        if self.user_photo:
            return self.user_photo.url
        return None

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=200)
    fine = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.book_name} - Due Date: {self.due_date}"


