from datetime import timedelta
from model.Year import Year, SlotType
from enum import Enum


class Clinic:

    SLOT_DURATION = 20

    def __init__(self, id, name, physical_address, dict_of_doctors, dict_of_rooms, business_hours):
        self.id = id
        self.name = name
        self.physical_address = physical_address
        self.doctors = dict_of_doctors
        self.rooms = dict_of_rooms
        self.business_hours = business_hours


class Room:
    def __init__(self, name, bookings_dict):
        self.name = name
        # booking dict is a key, value pair of datetime (appointment time), boolean (appointment is walk-in)
        self.bookings_dict = bookings_dict

    def get_week_availabilities_walk_in(self, room_truth_table):
        for truth_table_iterator in range(0, len(room_truth_table)):
            if room_truth_table[truth_table_iterator][0] is False:
                if room_truth_table[truth_table_iterator][1] in self.bookings_dict:
                    pass
            elif truth_table_iterator == 0 or truth_table_iterator == 1 or room_truth_table[truth_table_iterator][1] - room_truth_table[truth_table_iterator - 1][1] > timedelta(minutes=Clinic.SLOT_DURATION) or room_truth_table[truth_table_iterator][1] - room_truth_table[truth_table_iterator - 2][1] > timedelta(minutes=Clinic.SLOT_DURATION*2):
                # if this is the first or second slot of any day, mark this one as Available
                room_truth_table[truth_table_iterator][0] = True
            elif room_truth_table[truth_table_iterator - 1][1] in self.bookings_dict:
                # if the preceeding slot it a walk-in, mark this one as Available
                if self.bookings_dict[room_truth_table[truth_table_iterator - 1][1]] is True:
                    room_truth_table[truth_table_iterator][0] = True
                else:
                    pass
            elif room_truth_table[truth_table_iterator - 2][1] in self.bookings_dict:
                # if the slot that is two slots before this is marked as a walkin, mark this one as Available
                if self.bookings_dict[room_truth_table[truth_table_iterator - 2][1]] is True:
                    room_truth_table[truth_table_iterator][0] = True

        return room_truth_table


# hours must be 24 hr format with leading 0 : 08:00, NOT 8:00
class BusinessHours:
    def __init__(self, business_days, opening_hour, closing_hour):
        self.business_days = business_days
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour


class BusinessDays(Enum):
    SEVEN_DAYS = 1
    WEEKDAYS = 2
    NO_SUNDAYS = 3
