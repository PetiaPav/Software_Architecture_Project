from rest_framework import serializers
from ubersante.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'start_time', 'end_time', 'room_id', 'doctor_id', 'patient_id', 'clinic_id')
