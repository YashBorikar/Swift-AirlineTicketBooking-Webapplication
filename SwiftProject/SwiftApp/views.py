from django.shortcuts import render, get_object_or_404, redirect
from SwiftApp.models import AirlineDetail, AIRLINE_CHOICES, DEPARTURE_CHOICES, ARRIVAL_CHOICES, TIME_CHOICES, BookingDetail
from .forms import SignUpForm, BookingForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.core.mail import send_mail
import datetime
import decimal




def signup_view(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/login/')
    return render(request, 'SwiftApp/signup.html', {'form': form})

def logout_view(request):
    return render(request,'SwiftApp/logout.html')

def index(request):
    data={"DepartCity":DEPARTURE_CHOICES,"ArrivalCity":ARRIVAL_CHOICES}
    return render(request, 'SwiftApp/index.html', context=data)

def selectairline(request):
    if request.method=='GET':
        # Return City of Search Result
        departurecity = request.GET.get('departurecity')        # Retrieve Data from request
        arrivalcity = request.GET.get('arrivalcity')
        date = request.GET.get('date')
        try:
            returndep = DEPARTURE_CHOICES[int(departurecity)-1]     # Using Indexing of tuple and forward to select tag
            returnarr = ARRIVAL_CHOICES[int(arrivalcity)-1]
        except IndexError:
            returndep = "null"
            returnarr="null"

        # Fetch Required Objects
        airlinelist = AirlineDetail.objects.filter(Departure_City=departurecity).filter(Arrival_City=arrivalcity).order_by('Ticket_Price')
        count=airlinelist.count()

    data = {"DepartCity": DEPARTURE_CHOICES, "ArrivalCity": ARRIVAL_CHOICES, 'departurecity':returndep, 'arrivalcity':returnarr, 'airlinelist':airlinelist, 'date':date, 'count':count}
    return render(request, 'SwiftApp/airline-details.html/', context=data)

@login_required
def bookingdetails(request,id):
    BookedAirline = get_object_or_404(AirlineDetail, id=id)
    date = request.GET.get('date')
    form=BookingForm()

    data = {'bookedairline': BookedAirline, 'form':form, 'date':date}
    return render(request, 'SwiftApp/booking-details.html', context=data)

@login_required
def confirmbooking(request):
    bookid = request.POST.get('confirm-airline')
    user = request.user
    date = request.POST.get('date')
    redeem = request.POST.get('redeem')
    BookedAirline = AirlineDetail.objects.get(id=bookid)
    form = BookingForm()
    if request.method=='POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            new_booking = BookingDetail.objects.create(
                user=(user),
                Date=(date),
                Name=((form.cleaned_data['Title'])+' '+(form.cleaned_data['First_Name'])+' '+(form.cleaned_data['Second_Name'])),
                Email=(form.cleaned_data['Email']),
                Phone_Number=(form.cleaned_data['Contact_Number']),
                Address=((form.cleaned_data['Address'])+', '+(form.cleaned_data['City'])+', '+(form.cleaned_data['State'])+'-'+str(form.cleaned_data['Zip_Code'])),
                Flight_Details=BookedAirline,
                Final_Fare=BookedAirline.Ticket_Price
            )

            if redeem == "True":
                redeem_fair = (BookedAirline.Ticket_Price) * decimal.Decimal('.70')
                newredeem_fair = round(redeem_fair, 2)
                print(newredeem_fair)
                Book = BookingDetail.objects.get(id=new_booking.id)
                Book.Final_Fare=newredeem_fair
                Book.save()

            bookingdata=BookingDetail.objects.get(id=new_booking.id)

            # Email Forward
            subject = 'Flight Ticket Booking Details from Swift'
            message = 'Booking Details\n\n\nName of Passenger: {}\nTravel Date: {}\nAirline: {}\n' \
                      'Flight Number: \nTerminal: \nDeparture City: {}\nBoarding Time: {}\n' \
                      'Arrival City: {}\nArrival Time: {}\nFare: {}\nBooking Time:{}\n\n\nHappy Journey'.format(
                bookingdata.Name, bookingdata.Date, bookingdata.Flight_Details.get_Airline_display(),
                bookingdata.Flight_Details.get_Departure_City_display(), bookingdata.Flight_Details.get_Depart_Time_display(),
                bookingdata.Flight_Details.get_Arrival_City_display(), bookingdata.Flight_Details.get_Arrival_Time_display(),
                bookingdata.Flight_Details.Ticket_Price, bookingdata.Booktime)

            send_mail(subject, message, 'yashdev2411@gmail.com', [bookingdata.Email], fail_silently = True)


            return redirect('booking_detail',Name=bookingdata.Name,id=bookingdata.id,booktime=bookingdata.Booktime,journeydate=bookingdata.Date)

    data = {'bookedairline': BookedAirline, 'form': form, 'date':date}
    return render(request, 'SwiftApp/booking-details.html/', context=data)


@login_required()
def booking_details(request,Name,id,booktime,journeydate):
    post = get_object_or_404(BookingDetail, id=id, Name=Name, Booktime=booktime, Date=journeydate)
    return render(request, 'SwiftApp/confirm-booking.html', {'bookingdata': post})


@login_required
def userbooking(request):
    user=request.user
    bookinglist=BookingDetail.objects.filter(user=user).order_by('-Booktime')
    cancelbutton={}
    premondate = int(str(datetime.date.today())[5:7]+str(datetime.date.today())[8:])
    for book in bookinglist:
        mondate=int(((book.Date)[5:7])+((book.Date)[8:]))
        if mondate>premondate:
            cancelbutton[book.id]=True
        else:
            cancelbutton[book.id]=False
    return render(request, 'SwiftApp/userbooking.html',{'booking':bookinglist, 'cancel':cancelbutton})

@login_required
def deluserbooking(request, id):
    booking = get_object_or_404(BookingDetail, id=id)
    premondate = int(str(datetime.date.today())[5:7] + str(datetime.date.today())[8:])
    mondate = int(((booking.Date)[5:7]) + ((booking.Date)[8:]))
    if mondate > premondate:
        cancelbutton = True
    else:
        cancelbutton = False

    if request.method=='POST':
        booking.delete()
        return HttpResponseRedirect('/user-booking/')


    return render(request, 'SwiftApp/booking-delete.html', {'booking':booking, 'action': cancelbutton})



############## Admin Pannel #############

@login_required
@user_passes_test(lambda u: u.is_superuser)
def adminpanelindex(request):
    return render(request, 'SwiftApp/adminpanelindex.html')

class ABookingList(generic.ListView):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    model = BookingDetail
    ordering = ['-Booktime']

@login_required
@user_passes_test(lambda u: u.is_superuser)
def ABookingDetail(request,id):
    bookdetail=get_object_or_404(BookingDetail, id=id)
    return render(request, 'SwiftApp/bookingdetail_detail.html', {'book':bookdetail})

class AAirlineList(generic.ListView):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    model = AirlineDetail
    ordering = ['Airline','Departure_City']
    paginate_by = 30

class AAirlineUpdate(generic.UpdateView):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    model = AirlineDetail
    fields = ('Depart_Time', 'Arrival_Time', 'Ticket_Price', 'Terminal')

class AAirlineCreate(generic.CreateView):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    model = AirlineDetail
    fields = ('Airline', 'Departure_City', 'Depart_Time', 'Arrival_City', 'Arrival_Time', 'Terminal', 'Flight_Num', 'Ticket_Price')

class AAirlineDelete(generic.DeleteView):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    model = AirlineDetail
    success_url = reverse_lazy('airline-list')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def deluserbookingadmin(request, id):
    booking = get_object_or_404(BookingDetail, id=id)
    premondate = int(str(datetime.date.today())[5:7] + str(datetime.date.today())[8:])
    mondate = int(((booking.Date)[5:7]) + ((booking.Date)[8:]))
    if mondate > premondate:
        cancelbutton = True
    else:
        cancelbutton = False

    if request.method=='POST':
        booking.delete()
        return HttpResponseRedirect('/admin-list-booking/')

    return render(request, 'SwiftApp/booking-delete-admin.html', {'action': cancelbutton})



