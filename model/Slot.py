class Slot:
    def __init__(self):
        self.id = None
        # boolean to indicate whether the slot is being used as part of an hourly slot or as a 20 min slot 
        self.walk_in = None


class RoomSlot(Slot):
    def __init__(self):
        Slot.__init__(self)
        # boolean to indicated whether the slot has been marked as booked for an appointment
        self.booked = False
        # integer representing the doctor scheduled for the appointment
        self.doctor_id = None
        # integer representing the patient scheduled for the appointment
        self.patient_id = None


class DoctorSlot(Slot):
    def __init__(self):
        Slot.__init__(self)
        # boolean to indicate whether the doctor has marked this time as available to work
        self.available = False
