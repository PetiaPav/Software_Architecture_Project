from model.Clinic import Clinic, Room, BusinessHours, BusinessDays
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
        clinic_dict = self.tdg.get_clinics()
        for clinic in clinic_dict:
            clinic_id = clinic['id']
            clinic_physical_address = clinic['physical_address']
            clinic_name = clinic['name']
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

            all_doctors = self.mediator.get_all_doctors()

            for assignment in dict_of_doctor_clinic_assignments:
                for doctor in all_doctors:
                    if assignment['clinic_id'] == clinic_id and doctor.id == assignment['doctor_id']:
                        list_of_doctors.append(doctor)

            if dict_of_room_slots is not None:
                for room_slot in dict_of_room_slots:
                    week_index = Tools.get_week_index_from_slot_yearly_index(room_slot['slot_id'])
                    day_index = Tools.get_day_index_from_slot_yearly_index(room_slot['slot_id'])
                    slot_index = Tools.get_slot_index_from_slot_yearly_index(room_slot['slot_id'])
                    current_slot = list_of_rooms[room_slot['room_id']-1].schedule.week[week_index].day[day_index].slot[slot_index]
                    current_slot.id = room_slot["id"]
                    # a slot_yearly_index is a slot position in a 54 week calendar. Range: [0 - 27,215]
                    current_slot.slot_yearly_index = room_slot["slot_id"]
                    current_slot.patient_id = room_slot["patient_id"]
                    current_slot.doctor_id = room_slot["doctor_id"]
                    current_slot.booked = True
                    current_slot.walk_in = room_slot["walk_in"]

            # currently no database entries for business days
            business_hours = BusinessHours(BusinessDays.SEVEN_DAYS, clinic_start_time, clinic_end_time)
            self.catalog_dict[clinic_id] = Clinic(clinic_id, clinic_name, clinic_physical_address, list_of_doctors, list_of_rooms, business_hours)

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())
