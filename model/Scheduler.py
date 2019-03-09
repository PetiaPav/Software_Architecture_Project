from model.Tool import Tools
import random


class Scheduler:

    # expects date_time as string "2019-01-27T08:00:00", any day in the week will work
    @staticmethod
    def availability_finder(clinic, date_time, walk_in):
        # initialize an array where we will store tuples of available time slots (week_index, day_index, slot_index)
        available_slots = []
        week_index = Tools.get_week_index_from_date(date_time)

        # cycle through days of the week
        for day_index in range(0, 7):
            # step 1 : find an available room per time slot

            slot_index = Tools.get_slot_index_from_time(clinic.business_hours.opening_hour)

            while slot_index < Tools.get_slot_index_from_time(clinic.business_hours.closing_hour):
                # cycle through rooms of the clinic for an available room
                for room in range(0, len(clinic.rooms)):
                    if Scheduler.__room_is_not_booked(clinic.rooms[room], week_index, day_index, slot_index, walk_in):
                        # we found an available room, now lets find an available doctor
                        for doctor in range(0, len(clinic.doctors)):
                            # cycle through doctors to find availability
                            if Scheduler.__doctor_is_available(clinic.doctors[doctor].get_week_availability(week_index), day_index, slot_index, walk_in):
                                # we found a doctor with availability at this time
                                # we need to make sure the doctor is not booked during this time
                                if Scheduler.__doctor_is_not_booked(clinic.rooms, clinic.doctors[doctor], week_index, day_index, slot_index, walk_in):
                                    # we found an available time slot !
                                    available_slots.append((week_index, day_index, slot_index))
                                    # break out of this doctor for loop
                                    break
                    else:
                        continue
                    # we found an available doc in inner loop, break out of room loop
                    break
                # we did not find an available doctor / or broke out of the loop
                if walk_in is True:
                    slot_index += 1
                else:
                    slot_index += 3

            # out of the while loop

        # now we need to make our availablities into a format valid for fullcalendar
        return Tools.json_from_available_slots(available_slots, walk_in)

    @staticmethod
    def book_appointement(clinic, date_time, patient_id, walk_in):
        week_and_day_index = Tools.get_week_and_day_index_from_date(date_time)
        week_index = week_and_day_index[0]
        day_index = week_and_day_index[1]
        slot_index = Tools.get_slot_index_from_time(date_time[11:16])

        # find an empty room with randomness to avoid over booking any room
        for room in random.sample(range(len(clinic.rooms)), len(clinic.rooms)):
            if Scheduler.__room_is_not_booked(clinic.rooms[room], week_index, day_index, slot_index, walk_in):
                # find an available doctor with randomness to avoid over booking any doctor
                for doctor in random.sample(range(len(clinic.doctors)), len(clinic.doctors)):
                    if Scheduler.__doctor_is_available(clinic[doctor].get_week_availability(week_index), day_index, slot_index, walk_in):
                        if Scheduler.__doctor_is_not_booked(clinic.rooms, clinic.doctors[doctor], week_index, day_index, slot_index, walk_in):
                            return Scheduler.__mark_as_booked(clinic.rooms[room].schedule.week[week_index].day[day_index], slot_index, doctor.id, patient_id, walk_in)
        return None

    @staticmethod
    def __mark_as_booked(day, doctor_id, slot_index, patient_id, walk_in):
        appointment_slot = day.slot[slot_index]
        appointment_slot.booked = True
        appointment_slot.doctor_id = doctor_id
        appointment_slot.patient_id = patient_id
        appointment_slot.walk_in = walk_in
        if walk_in is False:
            for inner_slot_index in range(slot_index + 1, slot_index + 3):
                appointment_slot_extended = day.slot[inner_slot_index]
                appointment_slot_extended.booked = True
                appointment_slot_extended.doctor_id = doctor_id
                appointment_slot_extended.patient_id = patient_id
                appointment_slot.walk_in = walk_in
        # TODO update Database
        return appointment_slot

    @staticmethod
    def mark_as_available(clinic, appointment_slot):
        if appointment_slot.walk_in is False:
            week_day_index = Tools.get_week_and_day_index_from_date(Tools.get_date_time_from_slot_id(appointment_slot.slot_id)[0:10])
            for slot_index in range(Tools.get_slot_index_from_slot_id(appointment_slot.slot_id), Tools.get_slot_index_from_slot_id(appointment_slot.slot_id) + 2):
                slot_to_clear = clinic.rooms[appointment_slot.room_id-1].schedule.week[week_day_index[0]].day[week_day_index[1]].slot[slot_index]
                slot_to_clear.booked = False
                slot_to_clear.doctor_id = None
                slot_to_clear.patient_id = None
                slot_to_clear.walk_in = None
        else:
            appointment_slot.booked = False
            appointment_slot.doctor_id = None
            appointment_slot.patient_id = None
            appointment_slot.walk_in = None
        # TODO update Database
        return True

    @staticmethod
    def __doctor_is_not_booked(clinic_rooms, doctor, week_index, day_index, slot_index, walk_in):
        if walk_in is True:
            for room in range(0, len(clinic_rooms)):
                if clinic_rooms[room].schedule.week[week_index].day[day_index].slot[slot_index].booked is True and clinic_rooms[room].schedule.week[week_index].day[day_index].slot[slot_index].doctor_id is doctor.id:
                    # this doctor is already booked
                    return False
            # we made it through the list
            return True
        else:
            for room in range(0, len(clinic_rooms)):
                for inner_slot_index in range(slot_index, slot_index + 3):
                    if clinic_rooms[room].schedule.week[week_index].day[day_index].slot[inner_slot_index].booked is True and clinic_rooms[room].schedule.week[week_index].day[day_index].slot[inner_slot_index].doctor_id is doctor.id:
                        # this doctor is already booked
                        return False
                # we made it through the list
                return True

    @staticmethod
    def __room_is_not_booked(room, week_index, day_index, slot_index, walk_in):
        if walk_in is True:
            if room.schedule.week[week_index].day[day_index].slot[slot_index].booked is False:
                # this room is available at this time slot (room is not booked)
                return True
            else:
                return False

        else:
            for inner_slot_index in range(slot_index, slot_index + 3):
                if room.schedule.week[week_index].day[day_index].slot[inner_slot_index].booked is True:
                    # this room is already booked within the interval
                    break
                elif room.schedule.week[week_index].day[day_index].slot[inner_slot_index].booked is False and inner_slot_index is slot_index + 2:
                    # we made it to the end of the loop and the room is available
                    return True
        # we exited the loop without finding an available room, there are no available rooms for this time slot
        return False

    @staticmethod
    def __doctor_is_available(doctor_week_availability, day_index, slot_index, walk_in):
        if walk_in is True:
            if doctor_week_availability.day[day_index].slot[slot_index].available is True and doctor_week_availability.day[day_index].slot[slot_index].walk_in is True:
                return True
            else:
                return False

        else:
            for inner_slot_index in range(slot_index, slot_index + 3):
                if doctor_week_availability.day[day_index].slot[inner_slot_index].available is False or doctor_week_availability.day[day_index].slot[inner_slot_index].walk_in is True:
                    # this doctor is already booked within the interval or it is marked as a walk_in 
                    break
                elif doctor_week_availability.day[day_index].slot[inner_slot_index].available is True and inner_slot_index is slot_index + 2 and doctor_week_availability.day[day_index].slot[inner_slot_index].walk_in is False:
                    # we made it to the end of the loop and the doctor is available for a annual check-up
                    return True
            # we exited the loop without finding availability for this doctor, the doctor is not available for this time slot
            return False
