from django.contrib import admin
from home.models import Hall, HallAdmin, Booking, BookingAdmin


# Register your models here.
admin.site.register(Hall, HallAdmin)
admin.site.register(Booking, BookingAdmin)
