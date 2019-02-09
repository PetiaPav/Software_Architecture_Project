class Model:
    def __init__(self):
        None


class UserModel(Model):
    def __init__(self):
        None


class PatientModel(UserModel):
    def __init__(self):
        None


class DoctorModel(UserModel):
    def __init__(self):
        None


class NurseModel(UserModel):
    def __init__(self):
        None


class AdminModel(UserModel):
    def __init__(self):
        None


class LocationModel(Model):
    def __init__(self):
        None


class CityModel(LocationModel):
    def __init__(self):
        None


class ClinicModel(LocationModel):
    def __init__(self):
        None


class RoomModel(LocationModel):
    def __init__(self):
        None


class AppointmentModel(Model):
    def __init__(self):
        None
