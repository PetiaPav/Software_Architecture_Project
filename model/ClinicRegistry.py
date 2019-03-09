from model.Clinic import Clinic, Room, BusinessHours, BusinessDays


class ClinicRegistry:

    def __init__(self, tdg, doctor_catalog):
        self.tdg = tdg
        self.clinics = []
        self.populate(doctor_catalog)

    def populate(self, doctor_catalog):
        clinic_dict = self.tdg.get_clinics()
        for clinic in clinic_dict:
            clinic_id = clinic['id']
            clinic_name = clinic['name']
            clinic_physical_address = clinic['physical_address']
            clinic_start_time = clinic['start_time']
            clinic_end_time = clinic['end_time']
            clinic_slots_per_day = Clinic.get_slots_per_day(clinic_start_time, clinic_end_time, Clinic.SLOT_DURATION)

            dict_of_doctor_clinic_assignments = self.tdg.get_all_doctor_clinic_assignments()
            dict_of_rooms = self.tdg.get_rooms_by_clinic_id(clinic_id)

            list_of_doctors = []
            list_of_rooms = []

            for assignment in dict_of_doctor_clinic_assignments:
                for doctor in doctor_catalog:
                    if assignment['clinic_id'] == clinic_id and doctor.id == assignment['doctor_id']:
                        list_of_doctors.append(doctor)

            for room in dict_of_rooms:
                current_room = Room(clinic_slots_per_day)
                slot_id_index = 0
                for slot in room:
                    week_index = int(slot_id_index / (clinic_slots_per_day*7))
                    day_index = int((slot_id_index % (clinic_slots_per_day*7)) / clinic_slots_per_day)
                    slot_index = (slot_id_index % clinic_slots_per_day) % clinic_slots_per_day
                    current_slot = current_room.schedule.week[week_index].day[day_index].slot[slot_index]
                    current_slot.id = slot["id"]
                    current_slot.slot_id = slot["slot_id"]
                    current_slot.patient_id = slot["patient_id"]
                    current_slot.doctor_id = slot["doctor_id"]
                    current_slot.booked = slot["booked"]
                    current_slot.walk_in = slot["walk_in"]

                    slot_id_index = slot_id_index + 1
                list_of_rooms.append(current_room)
            # currently no database entries for this information
            business_hours = BusinessHours(BusinessDays.SEVEN_DAYS, 8, 20)
            self.clinics.append(Clinic(clinic_id, clinic_name, clinic_physical_address, list_of_doctors, list_of_rooms, business_hours))

    def get_by_id(self, id):
        for clinic in self.clinics:
            if id == clinic.id:
                return clinic
        return None
                