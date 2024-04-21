from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-hall/", views.addHall, name="addHall"),
    path("view-halls/", views.viewHalls, name="viewHalls"),
    path("remove-hall/<int:hallid>", views.removeHall, name="removeHall"),
    path("view-bookings/", views.viewBookings, name="viewBookings"),
    path("toggle-booking-status/<int:boolingid>", views.toggleBookingAcceptance, name="toggleBookingStatus"),
]
