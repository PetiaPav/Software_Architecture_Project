class Appointment():

    def __init__(self, id, clinic_id, room_id, doctor_id, patient_id, date_time, walk_in):
        self.id = id
        self.clinic_id = clinic_id
        self.room_id = room_id
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.date_time = date_time
        self.walk_in = walk_in
