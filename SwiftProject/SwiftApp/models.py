from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

AIRLINE_CHOICES = (
    ("1", "INDIGO"),
    ("2", "AIR INDIA"),
    ("3", "GO AIR"),
    ("4", "VISTARA"),
)

DEPARTURE_CHOICES = (
    ("1", "New Delhi (DEL)"),
    ("2", "Mumbai (BOM)"),
    ("3", "Bangalore (BLR)"),
    ("4", "Pune (PNQ)"),
    ("5", "Chennai (MMA)"),
    ("6", "Hyderabad (HYD)"),
)

ARRIVAL_CHOICES = (
    ("1", "New Delhi (DEL)"),
    ("2", "Mumbai (BOM)"),
    ("3", "Bangalore (BLR)"),
    ("4", "Pune (PNQ)"),
    ("5", "Chennai (MMA)"),
    ("6", "Hyderabad (HYD)"),
)

TIME_CHOICES = (
    ("1", "07:15"),
    ("2", "08:05"),
    ("3", "09:10"),
    ("4", "10:40"),
    ("5", "18:40"),
    ("6", "19:30"),
    ("7", "20:15"),
    ("8", "21:05"),
)

class AirlineDetail(models.Model):
    Airline = models.CharField(max_length=2, choices=AIRLINE_CHOICES)
    Flight_Num = models.CharField(max_length=7, help_text="Flight Number")
    Terminal = models.CharField(max_length=2)
    Departure_City = models.CharField(max_length=1, choices=DEPARTURE_CHOICES)
    Depart_Time = models.CharField(max_length=2, choices=TIME_CHOICES)
    Arrival_City = models.CharField(max_length=2, choices=ARRIVAL_CHOICES)
    Arrival_Time = models.CharField(max_length=2, choices=TIME_CHOICES)
    Ticket_Price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('airline-list')

class BookingDetail(models.Model):
    user = models.ForeignKey(User,related_name='user' ,on_delete=models.CASCADE)
    Date = models.CharField(max_length=11)
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Phone_Number = models.PositiveIntegerField()
    Address = models.CharField(max_length=200, default=None)
    Flight_Details = models.ForeignKey(AirlineDetail, related_name='airlinedetail', on_delete=models.CASCADE)
    Booktime = models.DateTimeField(auto_now_add=True)
    Final_Fare = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.Name

