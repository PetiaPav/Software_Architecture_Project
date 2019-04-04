from datetime import timedelta
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

    def get_room_by_id(self, id):
        return self.rooms[int(id)]

class Room:
    def __init__(self, id, name, bookings_dict):
        self.id = id
        self.name = name
        # booking dict is a key, value pair of datetime (appointment time), boolean (appointment is walk-in)
        self.bookings_dict = bookings_dict

    def add_booking(self, date_time, walk_in):
        if date_time is not None:
            self.bookings_dict[date_time] = walk_in

    def get_availability(self, date_time, walk_in):
        date_time_to_check = date_time
        if date_time_to_check in self.bookings_dict:  # Checking the requested time
            return None

        #  Checking if there are annual appointments in the next two slots
        date_time_to_check -= timedelta(minutes=20)
        if date_time_to_check in self.bookings_dict and self.bookings_dict[date_time_to_check] is False:
            return None

        date_time_to_check -= timedelta(minutes=20)
        if date_time_to_check in self.bookings_dict and self.bookings_dict[date_time_to_check] is False:
            return None

        if not walk_in:  # If appointment to be booked is annual, must also check two slots ahead
            date_time_to_check = date_time + timedelta(minutes=20)
            if date_time_to_check in self.bookings_dict:  # Checking the requested time
                return None
            date_time_to_check += timedelta(minutes=20)
            if date_time_to_check in self.bookings_dict:
                return None

        return self


class BusinessHours:
    def __init__(self, business_days, opening_time, closing_time):
        self.business_days = business_days
        self.opening_time = opening_time
        self.closing_time = closing_time


class BusinessDays(Enum):
    SEVEN_DAYS = 1
    WEEKDAYS = 2
    NO_SUNDAYS = 3
