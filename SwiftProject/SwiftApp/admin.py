from django.contrib import admin
from .models import AirlineDetail, BookingDetail

class AirlineAdmin(admin.ModelAdmin):
    list_display=['id','Airline', 'Departure_City','Depart_Time', 'Arrival_City', 'Arrival_Time', 'Flight_Num', 'Terminal', 'Ticket_Price']

class BookingAdmin(admin.ModelAdmin):
    list_display=['Name', 'user', 'Email', 'Phone_Number', 'Flight_Details', 'Booktime']

admin.site.register(AirlineDetail,AirlineAdmin)
admin.site.register(BookingDetail, BookingAdmin)