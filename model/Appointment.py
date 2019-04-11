from model.Subject import Subject


class Appointment(Subject):

    def __init__(self, id, clinic, room, doctor, patient, date_time, walk_in):
        super().__init__()
        self.id = id
        self.clinic = clinic
        self.room = room
        self.doctor = doctor
        self.patient = patient
        self.date_time = date_time
        self.walk_in = walk_in

    def notify(self, appointmentOperation):
        for observer in self._observers:
            observer.update(self, appointmentOperation)