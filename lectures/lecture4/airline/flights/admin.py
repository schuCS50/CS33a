from django.contrib import admin

from .models import Flight, Airport, Passenger

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id","origin", "destination", "duration")

class PassenderAdmin(admin.ModelAdmin):
    filter_horizontal = ("flight",)

admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassenderAdmin)