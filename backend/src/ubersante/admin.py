from django.contrib import admin
from ubersante.models import Appointment, Patient


# This is used to display Appointments as a table instead of a list in the admin dashboard
class AppointmentsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'start_time',
        'end_time',
        'room_id',
        'doctor_id',
        'patient_id'
        'clinic_id'
    )
    list_display_links = ('id', 'start_time')
    search_fields = ('start_time', 'content')
    list_per_page = 25


# This is used to display Patients in a table format in the admin dashboard
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'health_card_number',
        'first_name',
        'last_name',
        'phone_number',
        'email'
    )

    list_display_links = ('id', 'health_card_number')
    search_fields = ('health_card_number', 'content')
    list_per_page = 25


admin.site.register(Appointment, AppointmentsAdmin)
admin.site.register(Patient, PatientAdmin)

