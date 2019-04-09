from model.Clinic import Clinic, Room, BusinessHours, BusinessDays
from datetime import datetime
from model.Tools import Tools
import random


class ClinicRegistry:

    __instance_of_registry = None

    def __init__(self, mediator, tdg):
        self.tdg = tdg
        self.mediator = mediator
        self.catalog_dict = {}
        self.populate()

    @staticmethod
    def get_instance(mediator, tdg):
        if ClinicRegistry.__instance_of_registry is None:
            ClinicRegistry.__instance_of_registry = ClinicRegistry(mediator, tdg)
        return ClinicRegistry.__instance_of_registry

    def populate(self):
        tdg_clinic_dict = self.tdg.get_all_clinics()
        tdg_doctor_clinic_assignments = self.tdg.get_all_doctor_clinic_assignments()
        tdg_nurse_clinic_assignments = self.tdg.get_all_nurse_clinic_assignments()
        for clinic in tdg_clinic_dict:
            clinic_id = clinic['id']
            clinic_physical_address = clinic['physical_address']
            clinic_name = clinic['name']
            opening_time = clinic['start_time'].time()
            closing_time = clinic['end_time'].time()
            clinic_name = clinic['name']
            clinic_physical_address = clinic['physical_address']

            # get the doctors assigned to this clinic
            dict_of_doctors = {}
            for doctor_assignment in tdg_doctor_clinic_assignments:
                if int(doctor_assignment['clinic_id']) == clinic_id:
                    doctor_id = int(doctor_assignment['doctor_id'])
                    doctor = self.mediator.get_doctor_by_id(doctor_id)
                    if doctor is not None:
                        dict_of_doctors[doctor_id] = doctor
            # get the nurses assigned to this clinic
            dict_of_nurses = {}
            for nurse_assignment in tdg_nurse_clinic_assignments:
                if int(nurse_assignment['clinic_id']) == clinic_id:
                    nurse_id = int(nurse_assignment['nurse_id'])
                    nurse = self.mediator.get_nurse_by_id(nurse_id)
                    if nurse is not None:
                        dict_of_nurses[nurse_id] = nurse
            # get the rooms of this clinic
            dict_of_rooms = {}
            tdg_dict_of_rooms = self.tdg.get_rooms_by_clinic_id(clinic_id)
            if tdg_dict_of_rooms is not None:
                for room in tdg_dict_of_rooms:
                    room_id = room['id']
                    bookings_dict = {}
                    dict_of_rooms[room_id] = Room(room_id, room['name'], bookings_dict)

            business_hours = BusinessHours(BusinessDays.SEVEN_DAYS, opening_time, closing_time)
            self.catalog_dict[clinic_id] = Clinic(clinic_id, clinic_name, clinic_physical_address, dict_of_doctors, dict_of_nurses, dict_of_rooms, business_hours)

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())

    def register_clinic(self, form, doctors, nurses):
        start_time_list = form.start_time.data.split(':')
        end_time_list = form.end_time.data.split(':')
        start_time = datetime(2019, 1, 1, hour = int(start_time_list[0]), minute=int(start_time_list[1]), second=0)
        end_time = datetime(2019, 1, 1, hour = int(end_time_list[0]), minute=int(end_time_list[1]), second=0)
        clinic_id = self.tdg.insert_clinic(form.physical_address.data, form.name.data, start_time, end_time)
        self.tdg.insert_clinic_associations(clinic_id, doctors, nurses)
        room_dict = {}
        for counter in range(int(form.rooms.data)):
            room_name = str(random.randint(100, 1000))
            room_id = self.tdg.insert_room(room_name, clinic_id)
            bookings_dict = {}
            room_dict[room_id] = Room(room_id, room_name, bookings_dict)
        business_hours = BusinessHours(BusinessDays.SEVEN_DAYS, start_time.time(), end_time.time()) 
        self.catalog_dict[clinic_id] = Clinic(clinic_id, form.name.data, form.physical_address.data, doctors, nurses, room_dict, business_hours)

    def update_clinic(self, clinic, form, doctors, nurses):
        start_time_list = form.start_time.data.split(':')
        end_time_list = form.end_time.data.split(':')
        start_time = datetime(2019, 1, 1, hour = int(start_time_list[0]), minute=int(start_time_list[1]), second=0)
        end_time = datetime(2019, 1, 1, hour = int(end_time_list[0]), minute=int(end_time_list[1]), second=0)
        business_hours = BusinessHours(BusinessDays.SEVEN_DAYS, start_time.time(), end_time.time()) 
        self.tdg.update_clinic(clinic.id, form.physical_address.data, form.name.data, start_time, end_time)
        doctor_ids = clinic.doctors.keys()
        nurse_ids = clinic.nurses.keys()
        new_doctors = {}
        new_nurses = {}
        for doctor_id in doctors:
            if doctor_id in doctor_ids:
                continue
            new_doctors[doctor_id] = doctors[doctor_id]
        for nurse_id in nurses:
            if nurse_id in nurse_ids:
                continue
            new_nurses[nurse_id] = nurses[nurse_id]
        self.tdg.insert_clinic_associations(clinic.id, new_doctors, new_nurses)
        self.catalog_dict[clinic.id].name = form.name.data
        self.catalog_dict[clinic.id].physical_address = form.physical_address.data
        self.catalog_dict[clinic.id].business_hours = business_hours
        self.catalog_dict[clinic.id].doctors.update(new_doctors)
        self.catalog_dict[clinic.id].nurses.update(new_nurses)