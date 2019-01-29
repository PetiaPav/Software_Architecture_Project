from django.db import models

# Create your models here.


class Appointment(models.Model):
    time = models.DateTimeField(null=True)
    length = models.IntegerField(null=True)
    room = models.IntegerField(null=True)
    doctor = models.CharField(max_length=50, null=True)
    booked_by = models.IntegerField(null=True)  # TODO make into fk (patient)

    # can be defined to easily view item in browser
    # def __str__(self):
    #     return self.time
