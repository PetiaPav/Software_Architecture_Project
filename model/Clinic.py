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

    def get_availability(self, datetime, walk_in):
        times_to_check = [datetime, datetime - timedelta(minutes=20), datetime - timedelta(minutes=40)]
        for date_time in times_to_check:
            if date_time in self.bookings_dict:
                return None
        return self


# hours must be 24 hr format with leading 0 : 08:00, NOT 8:00
class BusinessHours:
    def __init__(self, business_days, opening_time, closing_time):
        self.business_days = business_days
        self.opening_time = opening_time
        self.closing_time = closing_time


class BusinessDays(Enum):
    SEVEN_DAYS = 1
    WEEKDAYS = 2
    NO_SUNDAYS = 3
