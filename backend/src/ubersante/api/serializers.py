from rest_framework import serializers
from ubersante.models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'time', 'length', 'room', 'doctor', 'booked_by')


