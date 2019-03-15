from model.Appointment import Appointment
from model.Scheduler import Scheduler
from model.Tool import Tools


class AppointmentRegistry:

    ID_COUNTER = 0

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
        all_clinics = self.mediator.get_all_clinics()
        for clinic in all_clinics:
            for room in clinic.rooms:
                for week in range(0, 54):
                    for day in range(0, 7):
                        slot_index = 0
                        current_slot = room.schedule.week[week].day[day].slot[slot_index]
                        if current_slot.booked is True:
                            new_appointment_id = self.get_new_id()
                            # add this appointment to the catalog
                            self.catalog_dict[new_appointment_id] = Appointment(new_appointment_id, clinic.id, current_slot)
                            # add the id to the patient associated with the appointment
                            self.mediator.get_patient_by_id(current_slot.patient_id).appointment_ids.append(new_appointment_id)
                            # add the id to the doctor asscociated with the appointment
                            self.mediator.get_doctor_by_id(current_slot.doctor_id).appointment_ids.append(new_appointment_id)
                            if current_slot.walk_in is False:
                                slot_index += 2
                        slot_index += 1

    @staticmethod
    def get_new_id():
        AppointmentRegistry.ID_COUNTER += 1
        return AppointmentRegistry.ID_COUNTER

    # expects date_time as string "2019-01-27T08:00:00"

    def add_appointment(self, patient_id, clinic_id, date_time, walk_in):
        new_appointment_slot = Scheduler.book_appointement(self.mediator.get_clinic_by_id(clinic_id), date_time, patient_id, walk_in)
        if new_appointment_slot is not None:
            appt_id = AppointmentRegistry.get_new_id()
            self.catalog_dict[appt_id] = (Appointment(appt_id, clinic_id, new_appointment_slot))
            # update the database
            self.tdg.update_room_slot(clinic_id, new_appointment_slot)
            return appt_id
        return None

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
            if appointment.appointment_slot.patient_id == patient_id:
                appointments_by_patient.append(appointment)
        if len(appointments_by_patient) > 0:
            return appointments_by_patient
        else:
            return None

    def get_appointments_by_doctor_id(self, doctor_id):
        appointments_by_doctor = []
        for appointment in self.catalog_dict:
            if appointment.appointment_slot.doctor_id == int(doctor_id):
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

    def delete_appointment(self, id):
        if int(id) in self.catalog_dict:
            appointment_to_delete = self.catalog_dict[int(id)]
            if appointment_to_delete.appointment_slot.id is not None:
                self.tdg.delete_room_slot(appointment_to_delete.appointment_slot.id)
            clinic_id = appointment_to_delete.clinic_id
            appointment_slot = appointment_to_delete.appointment_slot
            del self.catalog_dict[int(id)]
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
