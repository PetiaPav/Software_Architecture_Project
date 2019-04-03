from datetime import timedelta, datetime
from enum import Enum
from typing import Dict


class Clinic:
    SLOT_DURATION = 20

    def __init__(self, id: int, name: str, physical_address: str, dict_of_doctors, dict_of_rooms, business_hours):
        self.id = id
        self.name = name
        self.physical_address = physical_address
        self.doctors = dict_of_doctors
        self.rooms = dict_of_rooms
        self.business_hours = business_hours


class Room:
    def __init__(self, name: str, bookings_dict: Dict[datetime, bool]):
        self.name = name
        self.bookings_dict = bookings_dict

    def get_availability(self, date_time: datetime, walk_in: bool):
        date_time_to_check = date_time
        if date_time_to_check in self.bookings_dict:  # Checking the requested time
            return None

        #  Checking if there are annual appointments in the next two slots
        date_time_to_check -= timedelta(minutes=20)
        if date_time_to_check in self.bookings_dict:
            if self.bookings_dict[date_time_to_check] is False:
                return None
        else:
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
