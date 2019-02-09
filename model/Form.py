# TODO: from wtfforms import Form


class Serialize(Form):
    def __init__(self):
        None


class UserForm(Serialize):
    def __init__(self):
        None


class DoctorForm(UserForm):
    def __init__(self):
        None


class NurseForm(UserForm):
    def __init__(self):
        None


class PatientForm(UserForm):
    def __init__(self):
        None


class AdminForm(UserForm):
    def __init__(self):
        None


class LocationForm(Serialize):
    def __init__(self):
        None


class CityForm(LocationForm):
    def __init__(self):
        None


class ClinicForm(LocationForm):
    def __init__(self):
        None


class RoomForm(LocationForm):
    def __init__(self):
        None


class AppointmentForm(Serialize):
    def __init__(self):
        None
