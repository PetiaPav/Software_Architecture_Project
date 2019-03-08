class User:
    def __init__(self, id, first_name, last_name, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


class Patient(User):
    def __init__(self, id, first_name, last_name, password, health_card, birthday, gender, phone, physical_address, email, cart):
        User.__init__(self, id, first_name, last_name, password)
        self.health_card = health_card
        self.birthday = birthday
        self.gender = gender
        self.phone = phone
        self.physical_address = physical_address
        self.email = email
        self.cart = cart


class Nurse(User):
    def __init__(self, id, first_name, last_name, password, access_id):
        User.__init__(self, id, first_name, last_name, password)
        self.access_id = access_id


class Doctor(User):
    def __init__(self, id, first_name, last_name, password, physician_permit_number, specialty, city, availability, appointments):
        User.__init__(self, id, first_name, last_name, password)
        self.physician_permit_number = physician_permit_number
        self.specialty = specialty
        self.city = city
        self.availability = availability
        self.appointments = appointments


class DoctorMapper:
    def __init__(self, tdg):
        self.tdg = tdg
        self.catalog = []
        self.populate()

    def populate(self):
        doctor_dict = self.tdg.get_all_doctors()
        for doctor in doctor_dict:
            self.catalog.append(Doctor(doctor['id'], doctor['first_name'], doctor['last_name'], doctor['password'], doctor['permit_number'], doctor['specialty'], doctor['city'], None, None))
