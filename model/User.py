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
        self.catalog_dict = {}
        self.populate()

    def populate(self):
        doctor_dict = self.tdg.get_all_doctors()
        for doctor in doctor_dict:
            doctor_obj = Doctor(
                doctor['id'],
                doctor['first_name'],
                doctor['last_name'],
                doctor['password'],
                doctor['permit_number'],
                doctor['specialty'],
                doctor['city'],
                None,
                None
            )

            self.catalog_dict[doctor['id']] = doctor_obj

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())


class PatientMapper:
    def __init__(self, tdg):
        self.tdg = tdg
        self.catalog_dict = {}
        self.populate()

    def populate(self):
        patient_dict = self.tdg.get_all_patients()
        for patient in patient_dict:
            patient_obj = Patient(
                patient['id'],
                patient['first_name'],
                patient['last_name'],
                patient['password'],
                patient['health_card'],
                patient['birthday'],
                patient['gender'],
                patient['phone_number'],
                patient['physical_address'],
                patient['email'],
                None
            )
            self.catalog_dict[patient['id']] = patient_obj

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())


class NurseMapper:
    def __init__(self, tdg):
        self.tdg = tdg
        self.catalog_dict = {}
        self.populate()

    # id, first_name, last_name, password, access_id
    def populate(self):
        nurse_dict = self.tdg.get_all_nurses()
        for nurse in nurse_dict:
            nurse_obj = Nurse(
                nurse['id'],
                nurse['first_name'],
                nurse['last_name'],
                nurse['password'],
                nurse['access_id']
            )
            self.catalog_dict[nurse['id']] = nurse_obj

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())

