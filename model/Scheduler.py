from model.Tool import Tools


class Scheduler:

    @staticmethod
    def availability_finder(clinic, week_index, walk_in):
        # initialize an array where we will store tuples of available time slots (week_index, day_index, slot_index)
        available_slots = []

        # cycle through days of the week
        for day_index in range(0, 7):
            # step 1 : find an available room per time slot

            slot_index = 0

            while slot_index < 36:
                # cycle through rooms of the clinic for an available room
                for room in range(0, len(clinic.rooms)):
                    if Scheduler.__room_is_not_booked(clinic.rooms[room], week_index, day_index, slot_index, walk_in):
                        # we found an available room, now lets find an available doctor
                        for doctor in range(0, len(clinic.doctors)):
                            # cycle through doctors to find availability
                            if Scheduler.__doctor_is_available(clinic.doctors[doctor], day_index, slot_index, walk_in):
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
    def __doctor_is_available(doctor, day_index, slot_index, walk_in):
        if walk_in is True:
            if doctor.availability.day[day_index].slot[slot_index].available is True and doctor.availability.day[day_index].slot[slot_index].walk_in is True:
                return True
            else:
                return False

        else:
            for inner_slot_index in range(slot_index, slot_index + 3):
                if doctor.availability.day[day_index].slot[inner_slot_index].available is False or doctor.schedule.day[day_index].slot[inner_slot_index].walk_in is True:
                    # this doctor is already booked within the interval or it is marked as a walk_in 
                    break
                elif doctor.availability.day[day_index].slot[inner_slot_index].available is True and inner_slot_index is slot_index + 2 and doctor.schedule.day[day_index].slot[inner_slot_index].walk_in is False:
                    # we made it to the end of the loop and the doctor is available for a annual check-up
                    return True
            # we exited the loop without finding availability for this doctor, the doctor is not available for this time slot
            return False
