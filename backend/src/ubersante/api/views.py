from rest_framework.generics import ListAPIView, RetrieveAPIView
from ubersante.models import Appointment
from .serializers import AppointmentSerializer


class AppointmentListView(ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentDetailView(RetrieveAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
