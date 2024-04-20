from datetime import datetime
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


# Create your models here.
class Hall(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=False, max_length=500, default="")
    description = models.CharField(null=False, max_length=1500, default="")
    location = models.TextField(null=False, max_length=500, default="")
    capacity = models.IntegerField(null=False, default=0)
    images = models.ImageField(upload_to="HallImages", default="HallImages/default.jpg")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.location} {self.capacity}"


class HallAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
        "location",
        "capacity",
        "images",
        "created_at",
    ]



class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=False)
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="requestor_booking")
    provider = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="provider_booking")
    dean = models.TextField(null=False, default="")
    club = models.TextField(null=False, default="")
    department = models.TextField(null=False, default="")
    eventName = models.TextField(null=False, default="")
    eventDescription = models.CharField(null=False, max_length=1000, default="")
    startTime = models.DateTimeField(null=False, default=datetime.now)
    endTime = models.DateTimeField(null=False, default=datetime.now)
    approvedStatus = models.BooleanField(null=False, default=False)
    remarks = models.CharField(default="", max_length=500)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self) -> str:
        return f"{self.hall.name} requested by {self.requestor.first_name} from {self.provider.first_name} for event {self.eventName}"


class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "hall",
        "requestor",
        "provider",
        "dean",
        "club",
        "department",
        "eventName",
        "eventDescription",
        "startTime",
        "endTime",
        "approvedStatus",
        "remarks",
        "createdAt",
    ]
