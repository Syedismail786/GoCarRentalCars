from django.contrib import admin

from . models import Booking,Car

# Register your models here.
admin.site.register(Car)
admin.site.register(Booking)