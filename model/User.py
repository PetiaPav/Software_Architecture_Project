
from model.Year import Week, SlotType
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
    def __init__(self, id, first_name, last_name, password, health_card, birthday, gender, phone_number, physical_address, email, cart):
        User.__init__(self, id, first_name, last_name, password)
        self.health_card = health_card
        self.birthday = birthday
        self.gender = gender
        self.phone_number = phone_number
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

    def get_week_availability(self, week_index):
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
                current_slot.walk_in = Tools.int_to_bool(row['walk_in'])
                if row['walk_in'] == 0:
                    for inner_slot_index in range(row['slot_index'] + 1, row['slot_index'] + 3):
                        extra_slot = availability.day[row['day_index']].slot[inner_slot_index]
                        extra_slot.available = True
                        extra_slot.walk_in = False

            doctor_availabilities_special = self.tdg.get_doctor_availabilities_special(doctor['id'])

            availabilities_special = []

            for row in doctor_availabilities_special:
                available = True if row['available'] == 1 else False
                walk_in = True if row['walk_in'] == 1 else False
                special_availability = SpecialAvailability(row['id'], row['week_index'], row['day_index'], row['slot_index'], available, walk_in)
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


class SpecialAvailability:
    def __init__(self, id, week_index, day_index, slot_index, available, walk_in):
        self.id = id
        self.week_index = week_index
        self.day_index = day_index
        self.slot_index = slot_index
        self.available = available
        self.walk_in = walk_in
