from django.contrib import admin
from ubersante.models import Appointment

# This is used to display Appointments as a table instead of a list in the admin dashboard
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'time',
        'length',
        'room',
        'doctor',
        'booked_by'
    )
    list_display_links = ('id', 'time')
    search_fields = ('time', 'content')
    list_per_page = 25

admin.site.register(Appointment, AppointmentsAdmin)
