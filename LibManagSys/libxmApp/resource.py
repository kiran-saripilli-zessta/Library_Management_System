from datetime import timezone
from libxmApp.models import BookModel, Author, UserProfile, Genre, MemberModel, LoanModel
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field
from .fields import AvailabilityStatusField, ImageExportWidget, DueDateField



class BookModelResource(resources.ModelResource):
    book_author = fields.Field(column_name='book_author', attribute='book_author', widget=ForeignKeyWidget(Author, 'name'))
    genre_name = fields.Field(column_name='book_genre', attribute='book_genre__genre_name')
    availability_status = AvailabilityStatusField(column_name='availability_status', attribute='availability_status')
    class Meta:
        model = BookModel
        skip_unchanged = True  #handling duplicate data
        report_skipped = False #handling duplicate data
        fields = ('id', 'book_title', 'book_author', 'availability_status') 
        export_order = ('id', 'book_title', 'book_author', 'availability_status')

    def before_import_row(self, row, **kwargs):
        isbn = row.get('book_unique_isbn')
        existing_book = BookModel.objects.filter(book_unique_isbn=isbn)

        if existing_book:
            self._update_existing_record(existing_book, row)
        else:
            
            genre_name = row.get('book_genre')
            genre_instance, created = Genre.objects.get_or_create(genre_name=genre_name)
            row['book_genre'] = genre_instance
            author_name = row.get('book_author')
            author, created = Author.objects.get_or_create(name=author_name)
            row['book_author'] = author

            super().before_import_row(row, **kwargs)
    
    def _update_existing_record(self, existing_book, row):
        existing_book.book_title = row.get('book_title', existing_book.book_title)
        existing_book.book_author = row.get('book_author', existing_book.book_author)
        existing_book.book_genre = row.get('book_genre', existing_book.book_genre)
        existing_book.book_publisher = row.get('book_publisher', existing_book.book_publisher)
        existing_book.quantity_available = row.get('quantity_available', existing_book.quantity_available)
        existing_book.save()

class AuthorModelResource(resources.ModelResource):
    class Meta:
        model = Author
        skip_unchanged = True  
        report_skipped = False 
        fields = ('id','name')

class GenreModelResource(resources.ModelResource):
    class Meta:
        model = Genre
        skip_unchanged = True  
        report_skipped = False 
        fields = ('id','genre_name')

class UserProfileModelResource(resources.ModelResource):
    user_photo = fields.Field(column_name='user_photo', attribute='user_photo', widget=ImageExportWidget(), readonly=True)

    class Meta:
        model = UserProfile
        skip_unchanged = True
        report_skipped = False
        fields = ('id','username', 'email', 'user_photo')

class MemberModelResource(resources.ModelResource):
    member_name__username = fields.Field(column_name='member_name__username', attribute='member_name__username', readonly=True)
    book_titles = fields.Field(column_name='book_titles', attribute=None, readonly=True)
    total_late_fees = fields.Field(column_name='total_late_fees', attribute=None, readonly=True)

    class Meta:
        model = MemberModel
        fields = ('id', 'member_name__username', 'book_titles', 'total_late_fees')
        export_order = ('id', 'member_name__username', 'book_titles', 'total_late_fees')

    def dehydrate_book_titles(self, member):
        # Get a list of book titles issued by the member
        book_titles = [book.book_title for book in member.member_books_borrowed.all()]
        return ' , '.join(book_titles) if book_titles else None

    def dehydrate_total_late_fees(self, member):
        # Calculate total late fees for all borrowed books
        total_late_fees = sum(loan.fine for loan in member.loans.all())
        return total_late_fees


class LoanModelResource(resources.ModelResource):
    member = fields.Field(attribute='member__member_name__username', column_name='member')
    book_title = fields.Field(attribute='book__book_title', column_name='book_title')
    # due_date = DueDateField(column_name='due_date')  



    class Meta:
        model = LoanModel
        fields = ('id','member','book_title','due_date','return_date','fine','loan_status','loan_date')
        export_order = ('id','member','book_title','loan_date','return_date','due_date','loan_status','fine')



    def after_import_row(self, row, row_result, **kwargs):
        due_date_str = row.get('due_date')
        loan_status = row.get('loan_status')
        

        due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%d').date()

        print(f"Before - Due Date: {due_date}, Loan Status: {loan_status}")

        if due_date < timezone.now().date() and loan_status == 'On Loan':

            row['loan_status'] = 'Overdue'
            row_result.import_type = 'update' 

        print(f"After - Due Date: {due_date}, Loan Status: {loan_status}")

        super().after_import_row(row, row_result, **kwargs)
    

