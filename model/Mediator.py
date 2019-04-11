from model.Tdg import Tdg
from model.UserRegistry import UserRegistry
from model.ClinicRegistry import ClinicRegistry
from model.AppointmentRegistry import AppointmentRegistry
from model.Scheduler import Scheduler
from model.Tools import Tools


class Mediator:

    __instance_of_mediator = None

    def __init__(self, app, db_env):

        self.__tdg = Tdg(app, db_env)

        # Registy loading order matters
        print("Loading User Registry . . . ")
        self.__user_registry = UserRegistry.get_instance(self, self.__tdg)

        print("Loading Clinic Registry . . . ")
        self.__clinic_registry = ClinicRegistry.get_instance(self, self.__tdg)

        print("Loading Appointment Registry . . . ")
        self.__appointment_registry = AppointmentRegistry.get_instance(self, self.__tdg)

        self.__scheduler = Scheduler(self)

    @staticmethod
    def get_instance(app, db_env):
        if Mediator.__instance_of_mediator is None:
            Mediator.__instance_of_mediator = Mediator(app, db_env)
        return Mediator.__instance_of_mediator

    # Registry calls

    # # User calls

    def get_user_by_unique_login_identifier(self, unique_identifier, unique_identifier_value):
        if unique_identifier == "permit_number":
            return self.get_doctor_by_permit_number(unique_identifier_value)

        if unique_identifier == "email":
            return self.get_patient_by_email(unique_identifier_value)

        if unique_identifier == "access_id":
            return self.get_nurse_by_access_id(unique_identifier_value)

        return None

    # # # Patient calls

    def get_all_patients(self):
        return self.__user_registry.patient.get_all()

    def get_patient_by_id(self, patient_id):
        return self.__user_registry.patient.get_by_id(patient_id)

    def get_patient_by_email(self, email):
        return self.__user_registry.patient.get_by_email(email)

    def register_patient(self, email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address):
        self.__user_registry.patient.register(email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address)

    def update_patient(self, id, request):
        self.__user_registry.patient.update_patient(id, request)

    def get_patient_cart(self, patient_id):
        return self.__user_registry.patient.get_by_id(patient_id).cart

    def insert_patient_appointment_id(self, patient_id, new_appointment_id):
        self.__user_registry.patient.insert_appointment_ids(int(patient_id), [new_appointment_id])

    def insert_patient_batch_appointment_ids(self, patient_id, appointment_ids):
        self.__user_registry.patient.insert_appointment_ids(int(patient_id), appointment_ids)

    # # # Doctor calls

    def get_all_doctors(self):
        return self.__user_registry.doctor.get_all()

    def get_doctor_by_id(self, doctor_id):
        return self.__user_registry.doctor.get_by_id(doctor_id)

    def get_doctor_by_permit_number(self, permit_number):
        return self.__user_registry.doctor.get_by_permit_number(permit_number)

    def register_doctor(self, first_name, last_name, password, permit_number, specialty, city):
        self.__user_registry.doctor.register(first_name, last_name, password, permit_number, specialty, city)

    def get_doctor_schedule_by_week(self, doctor_id, date_time):
        return self.__user_registry.doctor.get_schedule_by_week(doctor_id, date_time)

    def set_doctor_generic_availability_from_json(self, doctor_id, json):
        self.__user_registry.doctor.set_generic_availability_from_json(doctor_id, json)

    def set_doctor_adjustments_from_json(self, doctor_id, json):
        self.__user_registry.doctor.set_adjustments_from_json(doctor_id, json)

    def add_doctor_appointment_id(self, doctor_id, new_appointment_id):
        self.__user_registry.doctor.add_appointment_id(int(doctor_id), new_appointment_id)

    def update_doctor_appointment_ids(self, appointments_created):
        self.__user_registry.doctor.update_appointment_ids(appointments_created)

    # # # Nurse calls

    def get_all_nurses(self):
        return self.__user_registry.nurse.get_all()

    def get_nurse_by_id(self, nurse_id):
        return self.__user_registry.nurse.get_by_id(nurse_id)

    def get_nurse_by_access_id(self, nurse_access_id):
        return self.__user_registry.nurse.get_by_access_id(nurse_access_id)

    def register_nurse(self, first_name, last_name, password, access_id):
        self.__user_registry.nurse.register(first_name, last_name, password, access_id)

    # # Clinic calls

    def get_all_clinics(self):
        return self.__clinic_registry.get_all()

    def get_clinic_by_id(self, clinic_id):
        return self.__clinic_registry.get_by_id(clinic_id)

    def register_clinic(self, form):
        self.__clinic_registry.register_clinic(form)

    def update_clinic(self, clinic, form):
        self.__clinic_registry.update_clinic(clinic, form)

    # # Appointment calls

    def get_appointment_by_id(self, appointment_id):
        return self.__appointment_registry.get_by_id(appointment_id)

    def add_appointment(self, patient_id, clinic_id, start_time, is_walk_in):
        return self.__appointment_registry.add_appointment(patient_id, clinic_id, start_time, is_walk_in)

    def add_appointment_batch(self, patient_id, accepted_ids):
        self.__appointment_registry.add_appointment_batch(patient_id, accepted_ids)

    def get_appointments_by_doctor_id(self, doctor_id):
        return self.__appointment_registry.get_appointments_by_doctor_id(doctor_id)

    def get_appointments_by_patient_id(self, patient_id):
        return self.__appointment_registry.get_appointments_by_patient_id(patient_id)

    def delete_appointment(self, appointment_id):
        self.__appointment_registry.delete_appointment(int(appointment_id))

    def update_appointment(self, appointment_id, clinic_id, new_date_time, walk_in):
        self.__appointment_registry.update_appointment(appointment_id, clinic_id, new_date_time, walk_in)

    def checkout_cart(self, cart_items, patient_id):
        return self.__appointment_registry.checkout_cart(cart_items, patient_id)

    def get_room_bookings_by_room_id(self, room_id):
        return self.__appointment_registry.get_room_bookings_by_room_id(room_id)

    # # Scheduler calls

    def find_availability(self, clinic_id, date_time, walk_in):
        return self.__scheduler.find_availability(clinic_id, date_time, walk_in)

    def confirm_availability(self, clinic_id, date_time, walk_in):
        return self.__scheduler.confirm_availability(clinic_id, date_time, walk_in)
