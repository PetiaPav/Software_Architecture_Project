from model.Tool import Tools


class Appointment():

    def __init__(self, id, clinic_id, appointment_slot):
        self.id = id
        self.clinic_id = clinic_id
        self.appointment_slot = appointment_slot
        # an appointment slot has attributes : id(clinic specific), doctor_id, patient_id, room_id, walk_in, booked 

    def get_date_time(self, slot_yearly_index):
        return Tools.get_date_time_from_slot_yearly_index(slot_yearly_index)
