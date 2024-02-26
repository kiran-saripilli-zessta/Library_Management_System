from import_export import fields
from import_export import resources, fields, widgets
from django.utils.html import format_html
from django.templatetags.static import static
from datetime import datetime
import pytz
# from datetime import timedelta
# from django.utils import timezone
# import datetime


current_datetime = datetime.now()
target_timezone = pytz.timezone('Asia/Kolkata')  

aware_datetime = target_timezone.localize(current_datetime)


class AvailabilityStatusField(fields.Field):
    def get_attribute(self, instance):
        # This method is called to get the value for the export field
        return "Available" if instance.quantity_available > 0 else "Out of Stock"

    def export(self, obj):
        # This method is called to get the export value for the field
        return self.get_attribute(obj)


class ImageExportWidget(widgets.Widget):
    def render(self, value, obj=None):
        
            # user_photo_url = obj.get_user_photo_url()
                # print("User Photo", user_photo_url)
        return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', value.url) if value else "Image Does not exists"
            

        return None

class DueDateField(fields.Field):
    def clean(self, value, row=None, *args, **kwargs):
        loan_date = row.get('loan_date')  # Make sure 'loan_date' matches the actual field name in your import file

        if loan_date:
            issue_date = timezone.make_aware(loan_date)
            print("Loan Date:", loan_date)
            print("Issue Date:", issue_date)

            return_date = issue_date + timedelta(days=7)
            due_date = issue_date + timedelta(days=10)

            result = due_date.date()  # Returning only the date portion for the field value
            print("Due Date:", result)
            
            # Convert the result to a string before returning
            return str(result)
        else:
            print("Warning: loan_date is None")

        return None