from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from .models import BookModel, LoanModel, Notification, UserProfile, MemberModel
from django.utils import timezone
from django.contrib import messages
from django.db.models.signals import Signal
from django.contrib.auth.signals import user_logged_in
from datetime import date, timedelta



@receiver(pre_save, sender=LoanModel)
@receiver(pre_delete, sender=LoanModel)
def update_book_availability(sender, instance, **kwargs):
    book = instance.book
    original_quantity = book.quantity_available

    borrowed_count = LoanModel.objects.filter(book=book, loan_status='On Loan').count()

    book.quantity_available = max(0, original_quantity - borrowed_count)
    print("Book Quantity :", book.quantity_available)

    book.save()




@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    if user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(username=user.username)
        loans = LoanModel.objects.filter(member__member_name=user_profile)

        current_date = timezone.now().date()  

        for loan in loans:
            issue_date = loan.loan_date
            return_date = loan.return_date

            if loan.due_date < current_date:
                fine = abs((current_date - loan.due_date).days) * 10

                loan.fine = fine
                loan.loan_status = 'Overdue'
                loan.save()

                notification = Notification.objects.create(
                    user=user,
                    book_name=loan.book.book_title,
                    fine=fine,
                    due_date=loan.due_date,
                )

    else:
        print("Please check your credentials")




    

        