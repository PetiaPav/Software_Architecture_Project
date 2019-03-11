from model.Clinic import Clinic, Room, BusinessHours, BusinessDays
from model.Tool import Tools


class ClinicRegistry:

    def __init__(self, tdg, doctor_catalog):
        self.tdg = tdg
        self.clinics = []
        self.populate(doctor_catalog)

    def populate(self, doctor_catalog):
        clinic_dict = self.tdg.get_clinics()
        for clinic in clinic_dict:
            clinic_id = clinic['id']
            # We should store start_time and end_time as varchar in the db
            clinic_start_time = Tools.int_to_24hr_format(int(clinic['start_time']))
            clinic_end_time = Tools.int_to_24hr_format(int(clinic['end_time']))
            clinic_name = clinic['name']
            clinic_physical_address = clinic['physical_address']


            dict_of_doctor_clinic_assignments = self.tdg.get_all_doctor_clinic_assignments()
            dict_of_room_slots = self.tdg.get_room_slots_by_clinic_id(clinic_id)

            list_of_doctors = []
            # will be modified when there are multiple rooms
            list_of_rooms = [Room(), Room(), Room(), Room(), Room()]

            for assignment in dict_of_doctor_clinic_assignments:
                for doctor in doctor_catalog:
                    if assignment['clinic_id'] == clinic_id and doctor.id == assignment['doctor_id']:
                        list_of_doctors.append(doctor)

            if dict_of_room_slots is not None:
                for room_slot in dict_of_room_slots:
                    current_slot = list_of_rooms[room_slot['room_id']-1].schedule.week[room_slot['week_index']].day[room_slot['day_index']].slot[room_slot['slot_index']]
                    current_slot.id = room_slot["id"]
                    # a slot_yearly_index is a slot position in a 54 week calendar. Range: [0 - 27,215]
                    current_slot.slot_yearly_index = Tools.get_slot_yearly_index_from_week_day_slot(room_slot['week_index'], room_slot['day_index'], room_slot['slot_index'])
                    current_slot.patient_id = room_slot["patient_id"]
                    current_slot.doctor_id = room_slot["doctor_id"]
                    current_slot.booked = True
                    current_slot.walk_in = room_slot["walk_in"]

            # currently no database entries for business days
            business_hours = BusinessHours(BusinessDays.SEVEN_DAYS, clinic_start_time, clinic_end_time)
            self.clinics.append(Clinic(clinic_id,clinic_name, clinic_physical_address, list_of_doctors, list_of_rooms, business_hours))

    def get_by_id(self, id):
        for clinic in self.clinics:
            if str(id) == str(clinic.id):
                return clinic
        return None
