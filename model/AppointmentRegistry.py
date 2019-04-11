from model.Appointment import Appointment
from datetime import datetime
from model.Tools import Tools


class AppointmentRegistry:

    __instance_of_registry = None

    def __init__(self, mediator, tdg):
        self.tdg = tdg
        self.mediator = mediator
        self.catalog_dict = {}
        self.populate()

    @staticmethod
    def get_test():
        return AppointmentRegistry.__instance_of_registry

    @staticmethod
    def get_instance(mediator, tdg):
        if AppointmentRegistry.__instance_of_registry is None:
            AppointmentRegistry.__instance_of_registry = AppointmentRegistry(mediator, tdg)
        return AppointmentRegistry.__instance_of_registry

    def populate(self):
        appointments = self.tdg.get_all_appointments()
        for appointment in appointments:

            appointment_id = int(appointment['id'])
            clinic = self.mediator.get_clinic_by_id(int(appointment['clinic_id']))
            room = clinic.get_room_by_id(int(appointment['room_id']))
            doctor = self.mediator.get_doctor_by_id(int(appointment['doctor_id']))
            patient = self.mediator.get_patient_by_id(int(appointment['patient_id']))
            date_time = appointment['date_time']
            walk_in = True if appointment['walk_in'] == 1 else False

            new_appointment = Appointment(appointment_id, clinic, room, doctor, patient, date_time, walk_in)
            self.catalog_dict[appointment_id] = new_appointment

            doctor.add_appointment(new_appointment)
            patient.add_appointment(new_appointment)
            room.add_booking(date_time, walk_in)

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())

    def get_appointments_by_clinic_id(self, clinic_id):
        clinic_appointments = []
        for appointment in self.catalog_dict.values():
            if appointment.clinic.id == clinic_id:
                clinic_appointments.append(appointment)
        if len(clinic_appointments) > 0:
            return clinic_appointments
        else:
            return None

    def get_appointments_by_patient_id(self, patient_id):
        patient_appointments = []
        for appointment in self.catalog_dict.values():
            if appointment.patient.id == int(patient_id):
                patient_appointments.append(appointment)
        if len(patient_appointments) > 0:
            return patient_appointments
        else:
            return None

    def get_appointments_by_doctor_id(self, doctor_id):
        doctor_appointments = []
        for appointment in self.catalog_dict.values():
            if appointment.doctor_id == int(doctor_id):
                doctor_appointments.append(appointment)
        if len(doctor_appointments) > 0:
            return doctor_appointments
        else:
            return None

    def get_room_bookings_by_room_id(self, room_id):
        room_bookings = {}
        for appointment in self.catalog_dict.values():
            if appointment.room.id == room_id:
                room_bookings[appointment.date_time] = appointment.walk_in
        return room_bookings

    def add_appointment(self, patient_id, clinic_id, date_time, walk_in):
        room_doctor_tuple = self.mediator.confirm_availability(clinic_id, date_time, walk_in, patient_id)
        if room_doctor_tuple is not None:
            clinic = self.mediator.get_clinic_by_id(clinic_id)
            room = room_doctor_tuple[0]
            doctor = room_doctor_tuple[1]
            patient = self.mediator.get_patient_by_id(patient_id)

            # Create new appointment with default id -1
            appointment = Appointment(-1, clinic, room, doctor, patient, date_time, walk_in)

            # Insert new appointment in APPOINTMENTS table in database
            appointment.id = self.tdg.insert_appointment(clinic_id, room.id, doctor.id, patient.id, date_time, walk_in)

            # Insert new appointment in catalog
            self.catalog_dict[appointment.id] = appointment

            # Add new appointment to the patient's list of appointments
            appointment.attach(patient)
            patient.add_appointment(appointment)

            # Add new appointment to the doctor's list of appointments
            appointment.attach(doctor)
            doctor.add_appointment(appointment)

            # Return reference to the newly created appointment
            return appointment
        return None

    def delete_appointment(self, appointment_id):
        if int(appointment_id) in self.catalog_dict:
            appointment_to_delete = self.catalog_dict[int(appointment_id)]
            if appointment_to_delete is not None:
                # Notify doctor and patient that their appointment is deleted
                appointment_to_delete.notify("delete")

                # Remove room booking
                room = appointment_to_delete.room
                date_time = appointment_to_delete.date_time
                room.remove_booking(date_time)

                # Remove appointment from doctor's appointment dict
                doctor = appointment_to_delete.doctor
                appointment_to_delete.detach(doctor)
                doctor.remove_appointment(appointment_to_delete)

                # Remove appointment from patient's appointment dict
                patient = appointment_to_delete.patient
                appointment_to_delete.detach(patient)
                patient.remove_appointment(appointment_to_delete)

                # Remove appointment from APPOINTMENTS table in db
                self.tdg.remove_appointment(appointment_to_delete.id)

                # Remove appointment from memory
                self.catalog_dict.pop(appointment_to_delete.id)

                return True
        return False

    def modify_appointment(self, appointment_id, new_date_time, walk_in):
        existing_appointment = self.get_by_id(int(appointment_id))
        if existing_appointment is not None:
            patient_id = existing_appointment.patent.id
            clinic_id = existing_appointment.clinic.id
            new_appointment = self.add_appointment(patient_id, clinic_id, new_date_time, walk_in)
            if new_appointment is not None:
                self.delete_appointment(int(appointment_id))
                return new_appointment
        return None

    def checkout_cart(self, item_list, patient_id):
        result = {
            'accepted_appointments_ids': [],
            'accepted_items': [],
            'accepted_items_is_walk_in': [],
            'rejected_items': []
        }
        for item in item_list:
            appointment = self.add_appointment(patient_id, item.clinic.id, item.start_time, item.is_walk_in)
            if appointment is not None:
                result['accepted_appointments_ids'].append(appointment.id)
                result['accepted_items'].append(item)
                result['accepted_items_is_walk_in'].append(item.is_walk_in)
            else:
                result['rejected_items'].append(item)
        return result

