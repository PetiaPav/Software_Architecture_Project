from model.Clinic import Clinic, Room, BusinessHours, BusinessDays
from datetime import datetime
from model.Tool import Tools


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
        tdg_doctor_clinic_assignments = self.tdg.get_doctor_clinic_assignments()
        for clinic in tdg_clinic_dict:
            clinic_id = clinic['id']
            clinic_physical_address = clinic['physical_address']
            clinic_name = clinic['name']
            opening_time = datetime.fromtimestamp(clinic['start_time'])
            closing_time = datetime.fromtimestamp(clinic['end_time'])
            clinic_name = clinic['name']
            clinic_physical_address = clinic['physical_address']

            # get the doctors assigned to this clinic
            dict_of_doctors = {}
            for doctor_assignment in tdg_doctor_clinic_assignments:
                if int(doctor_assignment['clinic_id']) == clinic_id:
                    doctor_id = int(doctor_assignment('doctor_id'))
                    doctor = self.mediator.get_doctor_by_id(doctor_id)
                    if doctor is not None:
                        dict_of_doctors[doctor_id] = doctor
            # get the rooms of this clinic
            dict_of_rooms = {}
            tdg_dict_of_rooms = self.tdg.get_rooms_by_clinic_id(clinic_id)
            if tdg_dict_of_rooms is not None:
                for room in tdg_dict_of_rooms:
                    room_id = room['id']
                    bookings_dict = {}
                    tdg_room_bookings = self.tdg.get_room_booking(room_id)
                    if tdg_room_bookings is not None:
                        for room_booking in tdg_room_bookings:
                            date_time = datetime.fromtimestamp(room_booking['date_time'])
                            walk_in = True if int(room_booking['walk_in']) == 1 else False
                            bookings_dict[date_time] = walk_in
                    dict_of_rooms[room_id] = Room(room['name'], bookings_dict)

            business_hours = BusinessHours(BusinessDays.SEVEN_DAYS, opening_time, closing_time)
            self.catalog_dict[clinic_id] = Clinic(clinic_id, clinic_name, clinic_physical_address, dict_of_doctors, dict_of_rooms, business_hours)

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())
