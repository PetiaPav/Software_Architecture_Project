from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Appointment(models.Model):
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    room_id = models.IntegerField(null=True)
    doctor_id = models.IntegerField(null=True)
    patient_id = models.IntegerField(null=True)  # TODO make into fk (patient)
    clinic_id = models.IntegerField(null=True)

    # can be defined to easily view item in browser
    def __str__(self):
        return "Clinic/Room: " + self.clinic_id + "/" + self.room_id + ", Patient: " + self.patient_id + " time: " +self.start_time


class User(AbstractUser):
    # Required fields for all users
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(max_length=255, unique=True)

    # Default toString()
    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.email


class Patient(User):
    # user = models.OneToOneField(parent_link=True, self, on_delete=models.CASCADE)
    health_card_number = models.CharField(max_length=100, blank=False, unique=True)
    birthday = models.CharField(max_length=100, blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('-', 'Do not wish to specify')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    physical_address = models.CharField(max_length=150, blank=False)

    # Override username field to use 'health_card_number' to login instead of 'username'
    USERNAME_FIELD = 'health_card_number'

    # Used to define table name in admin dashboard
    class Meta():
        verbose_name = 'Patient'


    # Default toString()
    def __str__(self):
        return self.health_card_number + " " + self.first_name + " " + self.last_name

