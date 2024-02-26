from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.apps import apps


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.current_username = request.user.username
            print(f"Current username: {request.current_username}")
        else:
            request.current_username = None

        response = self.get_response(request)
        return response
    

# class CheckBookAvailabilityMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.path == '/search-user-book-query/' and request.method == 'POST':
#             data = json.loads(request.body.decode('utf-8'))
#             user_query = data.get('userQuery', '').lower()

#             BookModel = apps.get_model('libxmApp', 'BookModel')

#             matching_books = BookModel.objects.filter(book_title__icontains=user_query)
#             print(matching_books)
#             if matching_books.exists():
#                 return JsonResponse({'status': 'success', 'message': 'Books available'})
#             else:
#                 print("In Else")
#                 return JsonResponse({'status': 'error', 'message': 'Book not available'})

#         response = self.get_response(request)
#         return response