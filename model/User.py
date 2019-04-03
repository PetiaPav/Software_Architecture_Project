
from datetime import timedelta, datetime
from typing import List, Dict

from model.Appointment import Appointment
from model.Tool import Tools
from model.FullCalendarEventWrapper import WrapDoctorGenericEvent
import copy
from flask import flash
import json


class User:
    def __init__(self, id, first_name: str, last_name: str, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


class Patient(User):
    def __init__(self, id, first_name: str, last_name: str, password, health_card, birthday, gender, phone_number, physical_address, email, cart, appointment_list):
        User.__init__(self, id, first_name, last_name, password)
        self.health_card = health_card
        self.birthday = birthday
        self.gender = gender
        self.phone_number = phone_number
        self.physical_address = physical_address
        self.email = email
        self.cart = cart
        self.appointment_list = appointment_list


class Nurse(User):
    def __init__(self, id, first_name, last_name, password, access_id):
        User.__init__(self, id, first_name, last_name, password)
        self.access_id = access_id


class Doctor(User):

    def __init__(self, id, first_name, last_name, password, permit_number, specialty, city, generic_week_availability: List[Dict[datetime.time, bool]], adjustment_list, appointment_dict: Dict[datetime, Appointment]):
        User.__init__(self, id, first_name, last_name, password)
        self.permit_number = permit_number
        self.specialty = specialty
        self.city = city
        self.generic_week_availability = generic_week_availability
        self.adjustment_list = adjustment_list
        self.appointment_dict = appointment_dict

    def get_availability(self, date_time: datetime, walk_in: bool):
        if date_time in self.appointment_dict:
            return None

        for adjustment in self.adjustment_list:
            if adjustment.date_time == date_time:
                if adjustment.operation_type_add:
                    if adjustment.walk_in == walk_in:
                        return self
                else:
                    return None

        generic_day_availability = self.generic_week_availability[date_time.weekday()]
        try:
            if generic_day_availability[date_time.time()] == walk_in:
                return self
            else:
                return None
        except KeyError:
            return None


class Adjustment:
    def __init__(self, id, date_time, operation_type_add, walk_in):
        self.id = id
        self.date_time = date_time
        # operation_type_add is a boolean that tells us if this availability should be added (True), or removed
        self.operation_type_add = operation_type_add
        self.walk_in = walk_in


class DoctorMapper:
    def __init__(self, mediator, tdg):
        self.mediator = mediator
        self.tdg = tdg
        self.catalog_dict = {}
        self.populate()

    def populate(self):
        doctor_dict = self.tdg.get_all_doctors()
        for doctor in doctor_dict:
            doctor_id = int(doctor['id'])
            doctor_generic_availabilities = self.tdg.get_doctor_generic_availabilities_by_id(doctor_id)
            generic_week_availability_list = [{}, {}, {}, {}, {}, {}, {}]
            if doctor_generic_availabilities is not None:
                for generic_availability_row in doctor_generic_availabilities:
                    date_time = generic_availability_row['date_time']
                    walk_in = True if generic_availability_row['walk_in'] == 1 else False
                    # Monday is 0, Sunday is 6 generic availabilities are stored in the week of September 30th, 2019
                    if date_time.day == 30:
                        generic_week_availability_list[0][date_time.time()] = walk_in
                    else:
                        generic_week_availability_list[date_time.day][date_time.time()] = walk_in

            doctor_adjustments = self.tdg.get_doctor_adjustments(doctor_id)
            adjustment_list = []

            if doctor_adjustments is not None:
                for adjustment_row in doctor_adjustments:
                    operation_type_add = True if adjustment_row['operation_type_add'] == 1 else False
                    walk_in = True if adjustment_row['walk_in'] == 1 else False
                    adjustment = Adjustment(int(adjustment_row['id']), adjustment_row['date_time'], operation_type_add, walk_in)
                    adjustment_list.append(adjustment)

            appointment_list = self.mediator.get_appointments_by_doctor_id(doctor_id)
            appointment_dict = {}
            for appointment in appointment_list:
                appointment_dict[appointment.date_time] = appointment

            doctor_obj = Doctor(
                doctor['id'],
                doctor['first_name'],
                doctor['last_name'],
                doctor['password'],
                doctor['permit_number'],
                doctor['specialty'],
                doctor['city'],
                generic_week_availability_list,
                adjustment_list,
                appointment_dict
            )

            self.catalog_dict[doctor_id] = doctor_obj

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())

    def get_by_permit_number(self, permit_number):
        for doctor in self.get_all():
            if str(doctor.permit_number) == permit_number:
                return doctor
        return None

    def register(self, first_name, last_name, password, permit_number, specialty, city):
        # record this doctor in the database and get a new id
        new_doctor_id = self.tdg.insert_doctor(first_name, last_name, password, permit_number, specialty, city)
        if new_doctor_id is not None:
            self.catalog_dict[new_doctor_id] = Doctor(new_doctor_id, first_name, last_name, password, permit_number, specialty, city, None, None, None)

    def set_generic_availability_from_json(self, doctor_id, json):
        doctor = self.get_by_id(int(doctor_id))
        # reset the current generic availability in working memory
        doctor.generic_week_availability = [{}, {}, {}, {}, {}, {}, {}]

        for event in json:
            event = WrapDoctorGenericEvent(event)
            doctor.generic_week_availability[event.day][event.time] = event.walk_in

        # update the tdg
        self.tdg.update_doctor_generic_availabilities(doctor.id, doctor.generic_week_availability)

    def set_special_availability_from_json(self, doctor_id, json):
        list_for_tdg = []
        list_of_ids_to_delete = []
        doctor = self.get_by_id(doctor_id)
        for event in json:
            walk_in = True if event['title'] == "Walk-in" else False
            week_index = Tools.get_week_index_from_date(event['time'])
            day_index = int(event['day'])
            slot_index = Tools.get_slot_index_from_time((event['time'])[11:16])
            available = True if event['id'] == 'new-availability' else False
            if event['id'] == 'removed-availability':
                for special_availability in doctor.availability_special:
                    if special_availability.slot_index == slot_index and special_availability.day_index == day_index and special_availability.week_index == week_index:
                        if special_availability.id is not None:
                            list_of_ids_to_delete.append(special_availability.id)
                        doctor.availability_special.remove(special_availability)
            doctor.availability_special.append(SpecialAvailability(None, week_index, day_index, slot_index, available, walk_in))
            list_for_tdg.append(SpecialAvailability("NULL", week_index, day_index, slot_index, available, walk_in))
        self.tdg.update_doctor_availabilities_special(int(doctor_id), list_for_tdg, list_of_ids_to_delete)

    def get_schedule_by_week(self, doctor_id, fullcalendar_datetime):
        doctor = self.get_by_id(doctor_id)
        date_time = Tools.convert_to_python_datetime(fullcalendar_datetime)
        week_start_time = self.week_start_from_date_time(date_time)
        week_end_time = self.week_end_from_week_start(week_start_time)

        requested_week_availabilities_dict = {}
        for day in range(0, len(doctor.generic_week_availability)):
            daily_availability = doctor.generic_week_availability[day]
            for time, walk_in in daily_availability.items():
                availability_date_time = week_start_time + timedelta(days=day)
                availability_date_time = (availability_date_time.year, availability_date_time.month, availability_date_time.day, time.hour, time.minute)
                requested_week_availabilities_dict[availability_date_time] = walk_in

            for adjustment in doctor.adjustment_list:
                if adjustment.date_time > week_start_time and adjustment.date_time < week_end_time:
                    if adjustment.operation_type_add is True:
                        requested_week_availabilities_dict[adjustment.date_time] = adjustment.walk_in
                    else:
                        if adjustment.date_time in requested_week_availabilities_dict:
                            del requested_week_availabilities_dict[adjustment.date_time] 

        requested_week_appointments_dict = {}
        for appointment in doctor.appointment_dict.values():
            if appointment.date_time > week_start_time and appointment.date_time < week_end_time:
                requested_week_appointments_dict[appointment.date_time] = appointment.walk_in

        event_source = Tools.json_from_doctor_week_availabilities(requested_week_availabilities_dict)
        event_source2 = Tools.json_from_doctor_week_appointments(requested_week_appointments_dict)
        for item in event_source2:
            event_source.append(item)
        return json.dumps(event_source)

    def update_appointment_ids(self, appointments):
        for appointment in appointments:
            doctor = self.get_by_id(appointment.appointment_slot.doctor_id)
            doctor.appointment_ids.append(appointment.id)

    def add_appointment_id(self, doctor_id, appointment_id):
        doctor = self.get_by_id(doctor_id)
        if appointment_id not in doctor.appointment_ids:
            doctor.appointment_ids.append(appointment_id)

    def delete_appointment(self, doctor_id, appointment_id):
        doctor = self.get_by_id(doctor_id)
        doctor.appointment_ids.remove(appointment_id)

    def week_start_from_date_time(self, date_time):
        week_start_time = date_time
        # Monday is 0 and Sunday is 6
        weekday = date_time.weekday()
        if weekday is not 0:
            week_start_time = date_time - timedelta(days=weekday)
        week_start_time = datetime(week_start_time.year, week_start_time.month, week_start_time.day, 0, 0)
        return week_start_time

    def week_end_from_week_start(self, week_start_time):
        week_end_time = week_start_time + timedelta(days=6)
        week_end_time = datetime(week_end_time.year, week_end_time.month, week_end_time.day, 23, 40)
        return week_end_time


class PatientMapper:
    def __init__(self, mediator, tdg):
        self.mediator = mediator
        self.tdg = tdg
        self.catalog_dict = {}
        self.populate()

    def populate(self):
        patient_dict = self.tdg.get_all_patients()
        for patient in patient_dict:
            patient_id = int(patient['id'])
            appointment_list = self.mediator.get_appointments_by_patient_id(patient_id)
            appointment_list = appointment_list if appointment_list is not None else []
            patient_obj = Patient(
                patient_id,
                patient['first_name'],
                patient['last_name'],
                patient['password'],
                patient['health_card'],
                patient['birthday'],
                patient['gender'],
                patient['phone_number'],
                patient['physical_address'],
                patient['email'],
                Cart(),
                appointment_list
            )
            self.catalog_dict[patient['id']] = patient_obj

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())

    def get_by_email(self, email):
        for patient in self.get_all():
            if patient.email == email:
                return patient
        return None

    def register(self, email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address):
        inserted_id = self.tdg.insert_patient(email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address)
        self.insert_patient(inserted_id, email, password, first_name, last_name, health_card, phone_number,
                                                 birthday, gender, physical_address)

    def update_patient(self, id, request):

        self.tdg.update_patient(
            id,
            request.form['first_name'][0:len(request.form['first_name'])],
            request.form['last_name'][0:len(request.form['last_name'])],
            request.form['health_card'][0:len(request.form['health_card'])],
            request.form['birthday'][0:len(request.form['birthday'])],
            request.form['gender'][0:len(request.form['gender'])],
            request.form['phone_number'][0:len(request.form['phone_number'])],
            request.form['physical_address'][0:len(request.form['physical_address'])],
            request.form['email'][0:len(request.form['email'])]
        )

        patient_obj = self.get_by_id(id)
        if patient_obj is not None:
            patient_obj.first_name = request.form['first_name'][0:len(request.form['first_name'])]
            patient_obj.last_name = request.form['last_name'][0:len(request.form['last_name'])],
            patient_obj.health_card = request.form['health_card'][0:len(request.form['health_card'])],
            patient_obj.birthday = request.form['birthday'][0:len(request.form['birthday'])],
            patient_obj.gender = request.form['gender'][0:len(request.form['gender'])],
            patient_obj.phone_number = request.form['phone_number'][0:len(request.form['phone_number'])],
            patient_obj.physical_address = request.form['physical_address'][0:len(request.form['physical_address'])],
            patient_obj.email = request.form['email'][0:len(request.form['email'])]

        flash(f'The patient account information (id {id}) has been modified.', 'success')

    def insert_appointment_ids(self, patient_id, appointment_ids):
        patient = self.get_by_id(patient_id)
        patient.appointment_ids = patient.appointment_ids + appointment_ids

    def insert_patient(self, patient_id, email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address):
        appointment_list = []
        patient_obj = Patient(
            patient_id,
            first_name,
            last_name,
            password,
            health_card,
            birthday,
            gender,
            phone_number,
            physical_address,
            email,
            Cart(),
            appointment_list
        )
        self.catalog_dict[patient_id] = patient_obj

    def delete_appointment(self, patient_id, appointment_id):
        patient = self.get_by_id(patient_id)
        patient.appointment_ids.remove(appointment_id)


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

    def get_by_access_id(self, access_id):
        for nurse in self.get_all():
            if nurse.access_id == access_id:
                return nurse
        return None

    def register(self, first_name, last_name, password, access_id):
        new_nurse_id = self.tdg.insert_nurse(first_name, last_name, password, access_id)
        if new_nurse_id is not None:
            self.catalog_dict[new_nurse_id] = Nurse(new_nurse_id, first_name, last_name, password, access_id)


class SpecialAvailability:
    def __init__(self, id, week_index, day_index, slot_index, available, walk_in):
        self.id = id
        self.week_index = week_index
        self.day_index = day_index
        self.slot_index = slot_index
        self.available = available
        self.walk_in = walk_in


class Cart:
    def __init__(self):
        self.item_dict = {}
        self.__id_counter = 0  # Internal ID of cart items, analogous to an autoincrementing ID as seen in popular DBs.

    def add(self, clinic, start_time, is_walk_in):
        if not self.__check_if_item_exists(clinic, start_time, is_walk_in):
            self.item_dict[self.__id_counter] = CartItem(self.__id_counter, clinic, start_time, is_walk_in, False)
            self.__id_counter += 1
            return True
        return False

    def __check_if_item_exists(self, clinic, start_time, is_walk_in):  # Checks if a cart item already exists.
        for item in self.item_dict.values():
            print(str(clinic.name) + ' ' + str(item.clinic.name) + ' ' + start_time + ' ' + item.start_time + ' ' + str(is_walk_in) + ' ' + str(item.is_walk_in))
            if clinic == item.clinic and start_time == item.start_time and is_walk_in == item.is_walk_in:
                return True
        return False

    def remove(self, item_id):
        try:
            self.item_dict.pop(item_id)
            return True
        except KeyError:
            return False

    def get_all(self):
        return list(self.item_dict.values())

    def batch_remove(self, item_list):  # Removes all items in a list of CartItems.
        for item in item_list:
            self.remove(item.item_id)

    def batch_mark_booked(self, item_list):  # Marks all items in a list of CartItems as booked.
        for item in item_list:
            item.is_booked = True


class CartItem:
    def __init__(self, item_id, clinic, start_time, is_walk_in, is_booked):
        self.item_id = item_id  # Internal cart item ID, not unique across multiple users.
        self.clinic = clinic
        self.start_time = start_time  # Stored as string
        self.is_walk_in = is_walk_in  # Stored as boolean
        self.is_booked = is_booked  # Stored as boolean
