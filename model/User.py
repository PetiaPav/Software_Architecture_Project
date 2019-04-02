
from datetime import timedelta, datetime
from model.Tool import Tools
import copy
from flask import flash
import json


class User:
    def __init__(self, id, first_name, last_name, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


class Patient(User):
    def __init__(self, id, first_name, last_name, password, health_card, birthday, gender, phone_number, physical_address, email, cart, appointment_list):
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

    def __init__(self, id, first_name, last_name, password, permit_number, specialty, city, generic_week_availability_list, adjustment_list, appointment_list):
        User.__init__(self, id, first_name, last_name, password)
        self.permit_number = permit_number
        self.specialty = specialty
        self.city = city
        # generic_week_availability_list contains dicts of datetime, walk_in-boolean pairs, index 0 is Monday, 6 is Sunday
        self.generic_week_availability_list = generic_week_availability_list
        # adjustments are objects defined in the Adjustment class below
        self.adjustment_list = adjustment_list
        self.appointment_list = appointment_list

    def get_week_availability_walk_in(self, doctor_truth_table):
        # step 1: create an array to store the current doctors availabilities
        doctor_availabilities = []

        # step 2: add generic availabilities, converted to the requested week, if they are walk-ins
        week_start_time = doctor_truth_table[0][1]
        for day in range(0, self.generic_week_availability_list):
            current_date_time = week_start_time + timedelta(days=day)
            # loop through the dict of availabilities looking for walk-in availabilities
            for date_time, walk_in in self.generic_week_availability_list[day]:
                if walk_in is True:
                    date_to_add = datetime(current_date_time.year, current_date_time.month, current_date_time.day, date_time.hour, date_time.minute)
                    doctor_availabilities.append(date_to_add)

        # step 3: add / remove adjustments
        for adjustment in self.adjustment_list:
            if adjustment.walk_in is True and week_start_time < adjustment.date_time and adjustment.date_time < week_start_time + timedelta(days=7):
                if adjustment.operation_type_add is True:
                    if adjustment.date_time not in doctor_availabilities:
                        doctor_availabilities.append(adjustment.date_time)
                else:
                    if adjustment.date_time in doctor_availabilities:
                        doctor_availabilities.remove(adjustment.date_time)

        # step 4: remove bookings
        if len(self.appointment_list) > 0:
            for appointment in self.appointment_list:
                if week_start_time < appointment.date_time and appointment.date_time < week_start_time + timedelta(days=7):
                    if appointment.date_time in doctor_availabilities:
                        doctor_availabilities.remove(appointment.date_time)

        # step 5: merge the availabilitis to the truth table
        for truth_table_iterator in range(0, len(doctor_truth_table)):
            if doctor_truth_table[truth_table_iterator][0] is False:
                if doctor_truth_table[truth_table_iterator][1] in doctor_availabilities:
                    doctor_truth_table[truth_table_iterator][0] = True

        return doctor_truth_table


class Adjustment():
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
            for gen_availabiliy_row in doctor_generic_availabilities:
                date_time = datetime.fromtimestamp(gen_availabiliy_row['date_time'])
                walk_in = True if gen_availabiliy_row['walk_in'] == 1 else False
                # Monday is 0, Sunday is 6 generic availabilities are stored in the week of September 30th, 2019
                if date_time.day == 30:
                    generic_week_availability_list[0][date_time] = walk_in
                else:
                    generic_week_availability_list[date_time.day][date_time] = walk_in

            doctor_adjustments = self.tdg.get_doctor_adjustments(doctor_id)
            adjustment_list = []

            for adjustment_row in doctor_adjustments:
                operation_type_add = True if adjustment_row['operation_type_add'] == 1 else False
                walk_in = True if adjustment_row['walk_in'] == 1 else False
                adjustment = Adjustment(int(adjustment_row['id']), datetime.fromtimestamp(adjustment_row['date_time']), operation_type_add, walk_in)
                adjustment_list.append(adjustment)

            appointment_list = self.mediator.get_appointments_by_doctor_id(doctor_id)

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
                appointment_list
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

    def set_availability_from_json(self, doctor_id, json):
        doctor = self.get_by_id(doctor_id)
        # reset the current availability in working memory
        doctor.availability = Week(SlotType.DOCTOR)
        list_for_tdg = []
        for event in json:
            walk_in = True if event['title'] == 'Walk-in' else False
            slot_index = Tools.get_slot_index_from_time(event['time'])
            current_slot = doctor.availability.day[int(event['day'])].slot[slot_index]
            current_slot.available = True
            current_slot.walk_in = walk_in
            list_for_tdg.append({'doctor_id': int(doctor_id), 'day': int(event['day']), 'slot_index': slot_index, 'walk_in': walk_in })
            if walk_in is False:
                for inner_slot_index in range(slot_index + 1, slot_index + 3):
                    current_slot = doctor.availability.day[int(event['day'])].slot[inner_slot_index]
                    current_slot.available = True
                    current_slot.walk_in = walk_in
        # update the tdg
        self.tdg.update_doctor_availability(int(doctor_id), list_for_tdg)

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

    def get_schedule_by_week(self, doctor_id, date_time, scheduled_appointments):
        doctor = self.get_by_id(doctor_id)
        availabilities = []
        new_scheduled_appointments = []
        week_index = Tools.get_week_index_from_date(date_time)
        week_availabilities = doctor.get_week_availability(week_index)
        if scheduled_appointments is not None:
            for appointment in scheduled_appointments:
                day_index = Tools.get_day_index_from_slot_yearly_index(appointment.appointment_slot.slot_yearly_index)
                slot_index = Tools.get_slot_index_from_slot_yearly_index(appointment.appointment_slot.slot_yearly_index)
                walk_in = appointment.appointment_slot.walk_in
                week_availabilities.day[day_index].slot[slot_index].available = False
                if walk_in is False:
                    for inner_slot_index in range(slot_index + 1, slot_index + 2):
                        week_availabilities.day[day_index].slot[inner_slot_index].available = False
                new_scheduled_appointments.append(((week_index, day_index, slot_index), walk_in))

        for day in range(0, 7):
            inner_slot_index = 0
            while inner_slot_index < 72:
                current_slot = week_availabilities.day[day].slot[inner_slot_index]
                if current_slot.available is True:
                    availabilities.append(((week_index, day, inner_slot_index), current_slot.walk_in))
                if current_slot.walk_in is False:
                    inner_slot_index += 2
                inner_slot_index += 1

        event_source = Tools.json_from_available_slots_doctor_available(availabilities)
        event_source2 = Tools.json_from_available_slots_doctor_scheduled(new_scheduled_appointments)
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
                Cart()
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
            Cart()
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
