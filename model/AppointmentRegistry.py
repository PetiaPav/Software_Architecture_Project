from model.Appointment import Appointment
from datetime import datetime
from model.Tool import Tools


class AppointmentRegistry:

    __instance_of_registry = None

    def __init__(self, mediator, tdg):
        self.tdg = tdg
        self.mediator = mediator
        self.catalog_dict = {}
        self.populate()

    @staticmethod
    def get_instance(mediator, tdg):
        if AppointmentRegistry.__instance_of_registry is None:
            AppointmentRegistry.__instance_of_registry = AppointmentRegistry(mediator, tdg)
        return AppointmentRegistry.__instance_of_registry

    def populate(self):
        appointments = self.tdg.get_all_appointments()
        for appointment in appointments:
            walk_in = True if appointment['walk_in'] == 1 else False
            new_appointment = Appointment(int(appointment['id']), int(appointment['clinic_id']), int(appointment['room_id']), int(appointment['doctor_id']), int(appointment['patient_id']), appointment['date_time'], walk_in)
            self.catalog_dict[new_appointment.id] = new_appointment

    def add_appointment(self, patient_id, clinic_id, date_time, walk_in):
        room_doctor_tuple = self.mediator.confirm_availability(clinic_id, date_time, walk_in)
        if new_appointment_slot is not None:
            new_appointment_id = AppointmentRegistry.get_new_id()
            self.catalog_dict[new_appointment_id] = (Appointment(new_appointment_id, clinic_id, new_appointment_slot))
            # update the database
            self.tdg.update_room_slot(clinic_id, new_appointment_slot)
            # update the patient's appointment list
            self.mediator.insert_patient_appointment_id(int(patient_id), new_appointment_id)
            # update the doctor's appointment list
            self.mediator.add_doctor_appointment_id(int(new_appointment_slot.doctor_id), new_appointment_id)

            return new_appointment_id
        return None

    def add_appointment_batch(self, accepted_ids):
        self.mediator.insert_patient_batch_appointment_ids(self.catalog_dict[accepted_ids[0]].appointment_slot.patient_id, accepted_ids)

        appointments_created = []
        for appt_id in accepted_ids:
            appointments_created.append(self.catalog_dict[appt_id])

        self.mediator.update_doctor_appointment_ids(appointments_created)

    def get_by_id(self, id):
        return self.catalog_dict[int(id)]

    def get_all(self):
        return list(self.catalog_dict.values())

    def get_appointments_by_clinic_id(self, clinic_id):
        appointments_by_clinic = []
        for appointment in self.catalog_dict:
            if appointment.clinic.id == clinic_id:
                appointments_by_clinic.append(appointment)
        if len(appointments_by_clinic) > 0:
            return appointments_by_clinic
        else:
            return None

    def get_appointments_by_patient_id(self, patient_id):
        appointments_by_patient = []
        for appointment in self.catalog_dict:
            if appointment.patient_id == int(patient_id):
                appointments_by_patient.append(appointment)
        if len(appointments_by_patient) > 0:
            return appointments_by_patient
        else:
            return None

    def get_appointments_by_doctor_id(self, doctor_id):
        appointments_by_doctor = []
        for appointment in self.catalog_dict:
            if appointment.doctor_id == int(doctor_id):
                appointments_by_doctor.append(appointment)
        if len(appointments_by_doctor) > 0:
            return appointments_by_doctor
        else:
            return None

    def get_appointments_by_doctor_id_and_week(self, doctor_id, week_index):
        appointments_by_doctor_and_week = self.get_appointments_by_doctor_id(int(doctor_id))
        if appointments_by_doctor_and_week is not None:
            appointments_by_doctor_and_week[:] = [appointment for appointment in appointments_by_doctor_and_week if Tools.get_week_index_from_slot_yearly_index(appointment.appointment_slot.slot_yearly_index) == week_index]
        return appointments_by_doctor_and_week

    def delete_appointment(self, appointment_id):
        if int(appointment_id) in self.catalog_dict:
            appointment_to_delete = self.catalog_dict[int(appointment_id)]
            if appointment_to_delete.appointment_slot.id is not None:
                self.tdg.delete_room_slot(appointment_to_delete.appointment_slot.id)
            clinic_id = appointment_to_delete.clinic_id
            appointment_slot = appointment_to_delete.appointment_slot
            # remove from the appointment registry
            del self.catalog_dict[int(appointment_id)]
            # remove from the patient's appointment list
            self.mediator.delete_patient_appointment(appointment_slot.patient_id, appointment_id)
            # remove from the doctor's appointment list
            self.mediator.delete_doctor_appointment(appointment_slot.doctor_id, appointment_id)
            # clear the room schedule
            return Scheduler.mark_as_available(self.mediator.get_clinic_by_id(clinic_id), appointment_slot)
        return False

    def modify_appointment(self, appointment_id, new_date_time, walk_in):
        existing_appointment = self.get_by_id(int(appointment_id))
        if existing_appointment is not None:
            patient_id = existing_appointment.appointment_slot.patient_id
            new_appointment_id = self.add_appointment(patient_id, existing_appointment.clinic_id, new_date_time, walk_in)
            if new_appointment_id is not None:
                self.delete_appointment(int(appointment_id))
                return new_appointment_id
        return None

    def checkout_cart(self, item_list, patient_id):
        result = {
            'accepted_appt_ids': [],
            'accepted_items': [],
            'accepted_items_is_walk_in': [],
            'rejected_items': []
        }
        for item in item_list:
            appt_id = self.add_appointment(patient_id, item.clinic.id, item.start_time, item.is_walk_in)
            if appt_id is not None:
                result['accepted_appt_ids'].append(appt_id)
                result['accepted_items'].append(item)
                result['accepted_items_is_walk_in'].append(item.is_walk_in)
            else:
                result['rejected_items'].append(item)
        return result
