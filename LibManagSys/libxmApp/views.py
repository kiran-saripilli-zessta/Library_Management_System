from django.shortcuts import render, redirect
from django.http import  HttpResponse
from .models import BookModel, Author, UserProfile, MemberModel
from .forms import BookForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from .serializer import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.core.files.storage import FileSystemStorage
from .serializer import UserModelSerializer
from django.db import transaction
from .exceptions import BookBorrowingException
import logging
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import boto3
from botocore.exceptions import NoCredentialsError
from urllib.parse import unquote




logger = logging.getLogger(__name__)



def index(request):
    return render(request, "libxmApp/index.html")

def get_authentication_status(request):
    print("User authenticated:", request.user.is_authenticated)
    return JsonResponse({'isAuthenticated': request.user.is_authenticated})

def signup(request):
    return render(request, "libxmApp/signup.html")


@login_required(login_url='/signup/')
def adminUI(request):
    return render(request, "libxmApp/adminUI.html")

@csrf_exempt
def loginUser(request):
    return render(request, "libxmApp/login.html")


def logout_page(request):
    logout(request)
    return('/login/')

@login_required(login_url='/login/')
def searchUserBookQuery(request):
    print("Inside View")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user_query = data.get('userQuery', '').lower()
        print("User Query", user_query)
        matching_books = BookModel.objects.filter(book_title__icontains=user_query)

        if matching_books.exists():
            return JsonResponse({'result': 'success', 'message': 'Books available'})
        else:
            return JsonResponse({'result': 'not_found', 'message': 'Book not available'})

    return JsonResponse({'result': 'error', 'message': 'Invalid request'})

@login_required(login_url='/login/')
def availableBooks(request):
    available_books = BookModel.objects.all()
    myAvailableBooksSerializer = BookModelSerializer(available_books, many=True)
    try:
        return render(request, 'libxmApp/books.html', {'available_books': myAvailableBooksSerializer.data})
    except Exception as e:
        print(f"Error in books view: {e}")
        raise

@login_required(login_url='/login/')
def newBooks(request):
    new_books = BookModel.objects.order_by('-created_at')[:5]
    myLatestBookSerializer = BookModelSerializer(new_books, many=True)
    try:
        return render(request, 'libxmApp/newArrival.html', {'new_books': myLatestBookSerializer.data})
    except Exception as e:
        print(f"Error in books view: {e}")
        raise


def issueBook(request):
    try:
        return render(request, 'libxmApp/bookIssue.html')
    except Exception as e:
        print(f"Error in author view: {e}")
        raise

@login_required(login_url='/login/')
def loanPageView(request):
    try:
        username = request.user.username  
        user_loans = LoanModel.objects.filter(member__member_name__username=username)
        on_loan_books = [loan for loan in user_loans if loan.loan_status == 'On Loan']
        returned_books = [loan for loan in user_loans if loan.loan_status == 'Returned']

        return render(request, 'libxmApp/loanPage.html', {'on_loan_books': on_loan_books, 'returned_books': returned_books})
    except Exception as e:
        print(f"Error in loan page view: {e}")
        raise


def returnBookView(request,loan_id):
    try:
        loan = get_object_or_404(LoanModel, id=loan_id)
        return render(request, 'libxmApp/returnBook.html',{'loan':loan})
    except Exception as e:
        print(f"Error in loan page view: {e}")
        raise


@transaction.atomic
def pay_return_book(request,loan_id):
    try:
        loan = LoanModel.objects.get(id=loan_id)
        
        loan = get_object_or_404(LoanModel, id=loan_id)

        # Check if the book has already been returned
        if loan.loan_status == 'Returned':
            print("Book has been already Returned")
            return JsonResponse({'status': 'error', 'message': 'Book has already been returned'})
        
        
        
        # Update book quantity in BookModel
        book = loan.book
        book.quantity_available += 1  # Assuming quantity_available is the field representing available quantity
        book.save()

        # Update loan status to 'Returned
        loan.loan_status = 'Returned'
        print("My Loan Status1",loan.loan_status)
        loan.fine = 0
        loan.save()
        print("My Loan Status2",loan.loan_status)

        # Redirect to a success page or any other page as needed
        return JsonResponse({'status': 'success', 'message': 'Book returned successfully'})

    except Exception as e:
        print(f"Error in pay_return_book view: {e}")
        return JsonResponse({'status': 'error', 'message': 'An error occurred'})

@login_required(login_url='/login/')
def viewNotifications(request):
    try:
        if request.user.is_authenticated:
            new_notifications = Notification.objects.filter(user=request.user)
            print("New Notifications:", new_notifications)

            # Get IDs of notifications already rendered on the page
            rendered_notification_ids = request.session.get('rendered_notification_ids', [])

            # Filter out notifications that have already been rendered
            filtered_notifications = new_notifications.exclude(id__in=rendered_notification_ids)

            # Update the list of rendered notification IDs
            rendered_notification_ids += list(filtered_notifications.values_list('id', flat=True))
            request.session['rendered_notification_ids'] = rendered_notification_ids

            return render(request, 'libxmApp/notifications.html', {'notifications': filtered_notifications})
        else:
            return redirect('/login/')

    except Exception as e:
        print(f"Error in notifications view: {e}")
        raise


@login_required(login_url='/login/')
def availableGenres(request):
    try:
        genres = Genre.objects.all()
        print("Genre", genres)
        return render(request, 'libxmApp/genre.html', {'genres': genres})
    except Exception as e:
        print(f"Error in author view: {e}")
        raise


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            user_data_json = request.body.decode('utf-8')
            print("Received Data:", user_data_json)
            
            user_data = json.loads(user_data_json)

            username = user_data.get('username')
            password = user_data.get('password')

            if not User.objects.filter(username=username).exists():
                messages.error(request, "Invalid Username")
                return JsonResponse({'result': 'error', 'message': 'Invalid Username'})

            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, 'Invalid Password')
                return JsonResponse({'result': 'error', 'message': 'Invalid Password'})
            else:
                login(request,user)
                request.session['logged_username'] = username 
                return JsonResponse({'result': 'success', 'message': 'Login successful'})


            # refresh = RefreshToken.for_user(user)                       #JWT Authentication
            # print("Refresh Token: ", str(refresh))
            # return JsonResponse({'result': 'success', 'message': 'Login successful', 'refresh':str(refresh), 'access':str(refresh.access_token)})

            # else:
            #     token, created = Token.objects.get_or_create(user=user)   #Token Authentication
            #     print("Token: " , token.key)  
            #     return JsonResponse({'result': 'success', 'message': 'Login successful'})
            
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'result': 'error', 'message': str(e)})

    return JsonResponse({'result': 'error', 'message': 'Invalid Request'})

@csrf_exempt
def delete_book(request):
    if request.method == 'GET':
        search_term = request.GET.get('term', '')
        book_to_delete = BookModel.objects.filter(book_title__iexact=search_term)
        if book_to_delete:
            book_serializer = BookModelSerializer(book_to_delete, many=True)
            book_to_delete.delete()
            return JsonResponse({'result': 'success', 'deleted_books': book_serializer.data})
        else:
            return JsonResponse({'result': 'not_found'})

    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def delete_user(request):
    if request.method == 'GET':
        search_term = request.GET.get('term', '')
        user_to_delete = UserProfile.objects.filter(email__iexact=search_term)
        if user_to_delete:
            user_serializer = UserModelSerializer(user_to_delete, many=True)
            user_to_delete.delete()
            return JsonResponse({'result': 'success', 'deleted_users': user_serializer.data})
        else:
            return JsonResponse({'result': 'not_found'})

    return JsonResponse({'error': 'Invalid request method'})

def get_user_details(request):
    if request.method == 'GET':
        entered_email = request.GET.get('email', '')
        user_profile = get_object_or_404(UserProfile, email=entered_email)

        user_serializer = UserModelSerializer(user_profile)
        user_details = user_serializer.data
        # print(user_details)

        return JsonResponse(user_details)

    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def update_user_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_email = data.get('userEmail')
            user_name = data.get('userName')
            user_pass = data.get('userPass')
            print("Data: ", user_email, user_name, user_pass)

            user_profile = UserProfile.objects.get(email=user_email)
            
            user_serializer = UserModelSerializer(user_profile, data={'username': user_name, 'password': user_pass}, partial=True)
            print(user_serializer)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse({'result': 'success'})
            else:
                return JsonResponse({'result': 'error', 'message': user_serializer.errors}, status=400)

        except UserProfile.DoesNotExist:
            return JsonResponse({'result': 'not_found'}, status=404)
        except Exception as e:
            return JsonResponse({'result': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'result': 'error'}, status=400)

@csrf_exempt
def add_book(request):
    if request.method == 'POST':
        try:
            book_data_json = request.body.decode('utf-8')
            print("Received Data:", book_data_json)
            
            book_data = json.loads(book_data_json)

            book_title = book_data.get('bookTitle')
            book_author_name = book_data.get('bookAuthor')  
            book_genre = book_data.get('bookGenre')
            book_unique_isbn = book_data.get('bookUniqueISBN')
            book_publisher = book_data.get('bookPublisher')
            quantity_available = book_data.get('bookQuantity')


            author_instance, created = Author.objects.get_or_create(name=book_author_name)
            genre_instance, created = Genre.objects.get_or_create(genre_name=book_genre)

            BookModel.objects.create(
                book_title=book_title,
                book_author=author_instance,
                book_genre=genre_instance,
                book_unique_isbn=book_unique_isbn,
                book_publisher=book_publisher,
                quantity_available = quantity_available
            )

            return JsonResponse({'result': 'success'})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'result': 'error', 'message': str(e)})

    return JsonResponse({'result': 'error'})


@csrf_exempt
def add_user(request):     #adding user through admin
    if request.method == 'POST':
        try:
            user_data_json = request.body.decode('utf-8')
            user_data = json.loads(user_data_json)

            user_username = user_data.get('userName')
            user_userpassword = user_data.get('userPass')  
            user_useremail = user_data.get('userEmail')

            hashed_password = make_password(user_userpassword)

            UserProfile.objects.create(
                username=user_username,
                password=hashed_password,
                email=user_useremail
            )

            return JsonResponse({'result': 'success'})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'result': 'error', 'message': str(e)})

    return JsonResponse({'result': 'error'})

def addBookToMember(request):
    if request.method == 'POST':
        try:
            book_user_json = request.body.decode('utf-8')
            bookUserData = json.loads(book_user_json)

            book_title = bookUserData['bookTitle']
            user_username = bookUserData['username']

            print("Received data:", book_title, user_username)

            try:
                user_profile = UserProfile.objects.get(username=user_username)
            except UserProfile.DoesNotExist:
                print("UserProfile matching query does not exist.")
                return JsonResponse({'result': 'error', 'message': 'UserProfile matching query does not exist. Please login with an authenticated username.'})

            try:
                book_instance = BookModel.objects.get(book_title=book_title)
            except BookModel.DoesNotExist:
                print("BookModel matching query does not exist.")
                return JsonResponse({'result': 'error', 'message': 'BookModel matching query does not exist.'})

            member, created = MemberModel.objects.get_or_create(
                member_name=user_profile
            )

            member.member_books_borrowed.add(book_instance)
            try:
                issue_book(request, member.id, book_instance.id)
            except BookBorrowingException as e:
                return JsonResponse({'result': 'error', 'message': str(e)},status=500)

            book_instance.quantity_available -= 1
            book_instance.save()


        
            print("Book added to member successfully.")
            return JsonResponse({'result': 'success', 'message': 'Book added to member successfully.'})

        except Exception as e:
            print("Error:", e)
            return JsonResponse({'result': 'error', 'message': str(e)})

    return JsonResponse({'result': 'error'})

@transaction.atomic
def issue_book(request, member_id, book_id):
    try:
        member = MemberModel.objects.get(pk=member_id)
        book = BookModel.objects.get(pk=book_id)
        user_profile = get_object_or_404(UserProfile, username=request.user.username)

        if book.quantity_available <= 0:
            raise BookBorrowingException("Book is out of stock")
        
        
        user_loans_count = LoanModel.objects.filter(member__member_name=user_profile, loan_status__in=['On Loan', 'Overdue']).count()
        borrowing_limit = 3 

        if user_loans_count >= borrowing_limit:
            raise BookBorrowingException("You have reached the borrowing limit")

        issue_date = timezone.now().date()
        return_date = issue_date + timedelta(days=7)  
        due_date = issue_date + timedelta(days=10)


        loan = LoanModel.objects.create(
            member=member,
            book=book,
            due_date=due_date,
            return_date=return_date,
            fine=Decimal('0.00'),
            loan_status='On Loan',
            loan_date=issue_date,
        )
        loan.save()

    except BookBorrowingException as e:
        print(f"Error in borrow_book view: {e}")
        # return JsonResponse({'status': 'error', 'message': str(e)})
        raise e
    
    except Exception as e:
        print(f"Error in borrow_book view: {e}")
        return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred'})


def checkUserBooks(request):
    if request.method == 'POST':
        try:
            data = request.body.decode('utf-8')
            json_data = json.loads(data)

            book_title = json_data.get('bookTitle', '')
            username = json_data.get('username', '')

            print("My Details", json_data)

            if book_title and username:
                try:
                    user_profile = UserProfile.objects.get(username=username)
                except UserProfile.DoesNotExist:
                    return JsonResponse({'hasBorrowed': False, 'error': 'User not found'})

                try:
                    book_instance = BookModel.objects.get(book_title=book_title)
                except BookModel.DoesNotExist:
                    return JsonResponse({'hasBorrowed': False, 'error': 'Book not found'})

                try:
                    member = MemberModel.objects.get(member_name=user_profile)
                except MemberModel.DoesNotExist:
                    return JsonResponse({'hasBorrowed': False, 'error': 'User has not borrowed this book'})

                has_borrowed = member.member_books_borrowed.filter(book=book_instance).exists()
                return JsonResponse({'hasBorrowed': has_borrowed})

            return JsonResponse({'hasBorrowed': False, 'error': 'Invalid data'})

        except Exception as e:
            return JsonResponse({'hasBorrowed': False, 'error': str(e)})

    return JsonResponse({'hasBorrowed': False, 'error': 'Invalid request method'})

@csrf_exempt
def addNewUser(request):     #adding user through signup
    if request.method == 'POST':
        try:
            user_username = request.POST.get('userName')
            user_userpassword = request.POST.get('passWord')
            user_useremail = request.POST.get('email')
            user_userimage = request.FILES.get('userImage')

            print(f"Username: {user_username}")
            print(f"Password: {user_userpassword}")
            print(f"Email: {user_useremail}")


            hashed_password = make_password(user_userpassword)

            if User.objects.filter(username=user_username).exists():
                return JsonResponse({'result': 'error', 'message': 'Username already exists'})

            user = User.objects.filter(username = user_username)
                

            user = User.objects.create(
                username=user_username,
                password=hashed_password,
                email = user_useremail
            )

            user.save()

            user_profile = UserProfile.objects.create(
                username=user_username,
                password=hashed_password,
                email=user_useremail
            )

            fs = FileSystemStorage(location='media/')
            filename = fs.save(user_userimage.name, user_userimage)
            user_profile.user_photo = filename

            bucket_name = 'libraryuserimages'

            if user_userimage:
                content = ContentFile(user_userimage.read())
                object_name = f"media/{user_userimage.name}"  # Adjust the S3 path as needed
                default_storage.save(object_name, content)

                # Update the user_profile with the S3 URL
                user_profile.user_photo = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
            
    
            user_profile.save()





            return JsonResponse({'result': 'success'})
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'result': 'error', 'message': str(e)})

    return JsonResponse({'result': 'error'})
    
@login_required(login_url='/login/')
def availableAuthors(request):
    try:
        authors = Author.objects.all()
        return render(request, 'libxmApp/authors.html', {'authors': authors})
    except Exception as e:
        print(f"Error in author view: {e}")
        raise

@login_required(login_url='/login/')
def books_details(request):
    books = BookModel.objects.all()
    myBooksSerializer = BookModelSerializer(books)
    return JsonResponse(myBooksSerializer.data)
    
def viewBooksAdmin(request):
    try:
        available_books2 = BookModel.objects.all()
        myAvailableBooksSerializer2 = BookModelSerializer(available_books2, many=True)
        return JsonResponse(myAvailableBooksSerializer2.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def viewUsersAdmin(request):
    try:
        available_users = UserProfile.objects.all()
        myAvailableUserSerializer = UserModelSerializer(available_users, many=True)
        return JsonResponse(myAvailableUserSerializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
