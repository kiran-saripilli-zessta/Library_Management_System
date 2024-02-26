from django.contrib import admin
from .models import BookModel, MemberModel, LoanModel, UserProfile, Author, Genre, Notification
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .resource import BookModelResource, AuthorModelResource, UserProfileModelResource, MemberModelResource, LoanModelResource





class BookAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_classes = [BookModelResource]
    list_display = ('id', 'book_title', 'display_author', 'book_genre')  # Add 'display_author' to list_display

    def display_author(self, obj):
        return obj.book_author.name if obj.book_author else ""  # Display author's name, handling the case where the author is not set

    display_author.short_description = 'Author'

class AuthorAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_classes = [AuthorModelResource]
    pass

class UserProfileAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_classes = [UserProfileModelResource]
    pass
    
class LoanModelAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_classes = [LoanModelResource]
    pass

class MemberModelAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_classes = [MemberModelResource]
    pass



admin.site.register(BookModel,BookAdmin)
admin.site.register(MemberModel, MemberModelAdmin)
admin.site.register(LoanModel,LoanModelAdmin)
admin.site.register(UserProfile,UserProfileAdmin )
admin.site.register(Author,AuthorAdmin)
admin.site.register(Genre)


admin.site.register(Notification)