from model.Year import Year, SlotType
from enum import Enum


class Clinic:

    SLOT_DURATION = 20

    def __init__(self, id, name, physical_address, list_of_doctors, list_of_rooms, business_hours):
        self.id = id
        self.name = name
        self.physical_address = physical_address
        self.doctors = list_of_doctors
        self.rooms = list_of_rooms
        self.business_hours = business_hours
        # we are multiplying the total hours open by 3 because there are 3 20-minute slots per hour.
        self.slots_per_day = Clinic.get_slots_per_day(business_hours.opening_hour, business_hours.closing_hour, Clinic.SLOT_DURATION)

    @staticmethod
    def get_slots_per_day(start_time, end_time, slot_duration):
        return (end_time - start_time) * (int(60/slot_duration))


class Room:
    def __init__(self):
        self.schedule = Year(SlotType.ROOM)


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
