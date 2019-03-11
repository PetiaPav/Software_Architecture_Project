from model.Appointment import Appointment
from model.Scheduler import Scheduler


class AppointmentRegistry:
    ID_COUNTER = 0

    def __init__(self, clinic_registry):
        self.catalog = []
        self.clinic_registry = clinic_registry
        self.populate(clinic_registry)

    # TODO
    def populate(self, clinic_registry):
        pass

    @staticmethod
    def get_new_id():
        AppointmentRegistry.ID_COUNTER += 1
        return AppointmentRegistry.ID_COUNTER

    # expects date_time as string "2019-01-27T08:00:00"
    def add_appointment(self, clinic, date_time, patient_id, walk_in):
        new_appointment = Scheduler.book_appointement(clinic, date_time, patient_id, walk_in)
        if new_appointment is not None:
            self.catalog.append(Appointment(AppointmentRegistry.get_new_id(), clinic.id, new_appointment))
            return True
        return False

    def get_appointment_by_id(self, appointment_id):
        for appointment in self.catalog:
            if appointment.id == appointment_id:
                return appointment
        return None

    def get_appointments_by_clinic_id(self, clinic_id):
        appointments_by_clinic = []
        for appointment in self.catalog:
            if appointment.clinic.id == clinic_id:
                appointments_by_clinic.append(appointment)
        if len(appointments_by_clinic) > 0:
            return appointments_by_clinic
        else:
            return None

    def get_appointments_by_patient_id(self, patient_id):
        appointments_by_patient = []
        for appointment in self.catalog:
            if appointment.appointment_slot.patient_id == patient_id:
                appointments_by_patient.append(appointment)
        if len(appointments_by_patient) > 0:
            return appointments_by_patient
        else:
            return None

    def get_appointments_by_doctor_id(self, doctor_id):
        appointments_by_doctor = []
        for appointment in self.catalog:
            if appointment.appointment_slot.doctor_id == int(doctor_id):
                appointments_by_doctor.append(appointment)
        if len(appointments_by_doctor) > 0:
            return appointments_by_doctor
        else:
            return None

    def get_appointments_by_doctor_id_and_week(self, doctor_id, week_index):
        appointments_by_doctor_and_week = self.get_appointments_by_doctor_id(int(doctor_id))
        appointments_by_doctor_and_week[:] = [appointment for appointment in appointments_by_doctor_and_week if Tools.get_week_index_from_slot_yearly_index(appointment.appointment_slot.slot_yearly_index) == week_index]
        return appointments_by_doctor_and_week

    def delete_appointment(self, id):
        appointment_to_delete = self.get_appointment_by_id(id)
        if appointment_to_delete is not None:
            return Scheduler.mark_as_available(self.clinic_registry.clinics[appointment_to_delete.clinic_id], appointment_to_delete.appointment_slot)
        return False

    def modify_appointment(self, id, clinic_number, doctor_id, patient_id, date_time, walk_in):
        pass
