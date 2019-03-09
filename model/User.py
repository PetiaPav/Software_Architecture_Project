from model.Year import Week, SlotType
import copy


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
    def __init__(self, id, first_name, last_name, password, permit_number, specialty, city, availability, availability_special):
        User.__init__(self, id, first_name, last_name, password)
        self.permit_number = permit_number
        self.specialty = specialty
        self.city = city
        self.availability = availability
        self.availability_special = availability_special

    def get_week_availabiliy(self, week_index):
        specific_week = copy.deepcopy(self.availability)
        for special in self.availability_special:
            if special.week_index == week_index:
                specific_week.day[special.day_index].slot[special.slot_index].available = special.available
                specific_week.day[special.day_index].slot[special.slot_index].walk_in = special.walk_in
                if special.walk_in is False:
                    specific_week.day[special.day_index].slot[special.slot_index+1].available = special.available
                    specific_week.day[special.day_index].slot[special.slot_index+1].walk_in = special.walk_in
                    specific_week.day[special.day_index].slot[special.slot_index+2].available = special.available
                    specific_week.day[special.day_index].slot[special.slot_index+2].walk_in = special.walk_in
        return specific_week

    def get_generic_week_availibility(self):
        pass


class DoctorMapper:
    def __init__(self, tdg):
        self.tdg = tdg
        self.catalog_dict = {}
        self.populate()

    def populate(self):
        doctor_dict = self.tdg.get_all_doctors()
        for doctor in doctor_dict:
            doctor_availabilities = self.tdg.get_doctor_availabilities(doctor['id'])

            # Build an empty week of availabilities
            availability = Week(SlotType.DOCTOR)

            # modify the slots that are marked as available in the database
            for row in doctor_availabilities:
                current_slot = availability.day[row['day_index']].slot[row['slot_index']]
                current_slot.available = True
                current_slot.walk_in = row['walk_in']
                if row['walk_in'] is False:
                    for inner_slot_index in range(row['slot_index'] + 1, row['slot_index'] + 3):
                        extra_slot = availability.day[row['day_index']].slot[inner_slot_index]
                        extra_slot.available = True
                        extra_slot.walk_in = False

            doctor_availabilities_special = self.tdg.get_doctor_availabilities_special(doctor['id'])

            availabilities_special = []

            for row in doctor_availabilities_special:
                special_availability = SpecialAvailability()
                special_availability.id = row['id']
                special_availability.week_index = row['week_index']
                special_availability.day_index = row['day_index']
                special_availability.slot_index = row['slot_index']
                special_availability.available = row['available']
                availabilities_special.append(special_availability)

            doctor_obj = Doctor(
                doctor['id'],
                doctor['first_name'],
                doctor['last_name'],
                doctor['password'],
                doctor['permit_number'],
                doctor['specialty'],
                doctor['city'],
                availability,
                availabilities_special
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


class SpecialAvailability:
    def __init__(self):
        self.id = None
        self.week_index = None
        self.day_index = None
        self.slot_index = None
        self.available = False
