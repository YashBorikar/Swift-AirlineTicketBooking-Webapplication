from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('signup/', views.signup_view),
    path('logout/', views.logout_view),
    path('select-airline/', views.selectairline),
    path('booking-details/<int:id>', views.bookingdetails),
    path('confirm-booking/', views.confirmbooking),
    path('flight-booking-details/<str:Name>/<int:id>/<str:booktime>/<str:journeydate>', views.booking_details, name="booking_detail"),
    path('user-booking/', views.userbooking, name="userbooking"),
    path('user-booking/cancel-booking/<int:id>',views.deluserbooking),
    path('admin-user-booking/cancel-booking/<int:id>',views.deluserbookingadmin),
    path('admin-pannel-index/', views.adminpanelindex),
    path('admin-list-booking/', views.ABookingList.as_view()),
    path('admin-detail-booking/<int:id>', views.ABookingDetail),
    path('admin-list-airline/', views.AAirlineList.as_view(), name="airline-list"),
    path('admin-update-airline/<int:pk>', views.AAirlineUpdate.as_view()),
    path('admin-create-airline/', views.AAirlineCreate.as_view()),
    path('admin-delete-airline/<int:pk>', views.AAirlineDelete.as_view()),
]