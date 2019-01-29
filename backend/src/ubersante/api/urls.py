from django.urls import path
from .views import AppointmentListView, AppointmentDetailView

urlpatterns = [
    path('', AppointmentListView.as_view()),
    path('<pk>', AppointmentDetailView.as_view())
]