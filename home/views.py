from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home.models import Hall, Booking

from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, "home/index.html")


@login_required(login_url="/auth/login/")
def addHall(request):
    if request.user.is_authenticated and (
        request.user.is_staff or request.user.is_superuser
    ):
        if request.method == "POST":
            try:
                name = request.POST["name"]
                description = request.POST["description"]
                location = request.POST["location"]
                capacity = request.POST["capacity"]
                images = request.FILES["images"]
                newHall = Hall(
                    name=name,
                    description=description,
                    location=location,
                    capacity=capacity,
                    images=images,
                )
                newHall.save()
                messages.success(request, "Hall added successfully")
                return redirect("addHall")
            except:
                messages.error(request, "Something went wrong")
                return redirect("addHall")
        else:
            return render(request, "home/addHall.html")
    else:
        messages.error(request, "Must be staff or superuser")
        return redirect("signin")


@login_required(login_url="/auth/login/")
def removeHall(request, hallid):
    if request.user.is_authenticated and (
        request.user.is_staff or request.user.is_superuser
    ):
        hall = Hall.objects.get(id=hallid)
        hall.delete()
        messages.success(request, "Hall removed successfully")
        return redirect("viewHalls")


@login_required(login_url="/auth/login/")
def viewHalls(request):
    if request.method == "POST":
        eventdate = request.POST.get("event_date")
        startTime = request.POST.get("start_time")
        endTime = request.POST.get("end_time")
        print(eventdate, startTime, endTime)

        bookingsOnTime = Booking.objects.filter(
            startTime__gte=startTime,
            endTime__lte=endTime,
            dateOfEvent=eventdate,
            approvedStatus=True,
        ).all()

        print(bookingsOnTime)
        hallsAvaliable = Hall.objects.exclude(
            id__in=[i.hall.id for i in bookingsOnTime]
        ).all()
        print(hallsAvaliable)
        return render(
            request, "home/viewHalls.html", {"hallsAvailable": hallsAvaliable}
        )
    else:
        hallsAvaliable = Hall.objects.all()
        print(hallsAvaliable)
        return render(
            request, "home/viewHalls.html", {"hallsAvailable": hallsAvaliable}
        )


# class Booking(models.Model):
#     id = models.AutoField(primary_key=True)
#     hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=False)
#     requestor = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="requestor_booking")
#     provider = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="provider_booking")
#     dean = models.TextField(null=False, default="")
#     club = models.TextField(null=False, default="")
#     department = models.TextField(null=False, default="")
#     eventName = models.TextField(null=False, default="")
#     eventDescription = models.TextField(null=False, max_length=1000, default="")
#     startTime = models.DateTimeField(null=False, default=datetime.now)
#     endTime = models.DateTimeField(null=False, default=datetime.now)
#     approvedStatus = models.BooleanField(null=False, default=False)
#     remarks = models.TextField(default="", max_length=500)
#     createdAt = models.DateTimeField(auto_now_add=True, null=False)


#     def __str__(self) -> str:
#         return f"{self.hall.name} requested by {self.requestor.first_name} from {self.provider.first_name} for event {self.eventName}"
@login_required(login_url="/auth/login/")
def addBooking(request):
    if request.method == "POST":
        try:
            hall = Hall.objects.get(id=int(request.POST.get("hall")))
            requestor = request.user
            provider = User.objects.get(id=int(request.POST.get("provider")))
            dean = request.POST.get("dean")
            club = request.POST.get("club")
            department = request.POST.get("department")
            eventName = request.POST.get("event_name")
            eventDescription = request.POST.get("event_description")
            dateOfEvent = request.POST.get("dateOfEvent")
            startTime = request.POST.get("start_time")
            endTime = request.POST.get("end_time")
            bookingsOnTime = bookingsOnTime = Booking.objects.filter(
                startTime__gte=startTime,
                endTime__lte=endTime,
                dateOfEvent=dateOfEvent,
                approvedStatus=True,
            ).all()
            for booking in bookingsOnTime:
                if booking.hall == hall:
                    messages.error(request, "Already Booked")
                    return redirect("addBooking")
                if datetime.strptime(startTime, "%H:%M") >= datetime.strptime(
                    endTime, "%H:%M"
                ):
                    messages.error(request, "Start time must be before end time")
                    return redirect("addBooking")
            booking = Booking(
                hall=hall,
                requestor=requestor,
                provider=provider,
                dean=dean,
                club=club,
                department=department,
                eventName=eventName,
                eventDescription=eventDescription,
                dateOfEvent=dateOfEvent,
                startTime=startTime,
                endTime=endTime,
            )
            messages.success(request, "Hall booking request sent successfully!")
            return redirect("addBooking")
        except:
            messages.error(request, "Something went wrong")
            return redirect("addBooking")
    else:
        hallsAvaliable = Hall.objects.all()
        requestors = User.objects.filter(is_staff=True).all()
        return render(
            request,
            "home/addBooking.html",
            {"hallsAvaliable": hallsAvaliable, "requestors": requestors},
        )


@login_required(login_url="/auth/login/")
def viewBookings(request):
    if request.user.is_staff or request.user.is_superuser:
        bookings = Booking.objects.filter(dateOfEvent__gte=datetime.now).all()
        return render(request, "home/viewBookings.html", {"bookings": bookings})
    else:
        bookings = Booking.objects.filter(
            dateOfEvent__gte=datetime.now, requestor=request.user
        ).all()
        return render(request, "home/viewBookings.html", {"bookings": bookings})


@login_required(login_url="/auth/login/")
def toggleBookingAcceptance(request, bookingid):
    if request.user.is_staff or request.user.is_superuser:
        booking = Booking.objects.get(id=bookingid)
        if booking.approvedStatus:
            booking.approvedStatus = False
        else:
            booking.approvedStatus = True
        booking.save()
        messages.success(
            request, f"Approved Status changed to {booking.approvedStatus}"
        )
        return redirect("viewBookings")
    else:
        messages.error(request, "Must be staff or superuser")
        return redirect("signin")
