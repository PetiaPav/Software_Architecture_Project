from model.Year import Year, SlotType
from enum import Enum


class Clinic:
    def __init__(self, list_of_doctors, number_of_rooms, business_hours):
        self.doctors = list_of_doctors
        self.rooms = []
        self.business_hours = business_hours
        # we are multiplying the total hours open by 3 because there are 3 20 minute slots per hour.
        slots_per_day = (business_hours.closing_hour - business_hours.opening_hour) * 3

        # once the database is implemented, the structure would be populated from the database
        for x in range(0, number_of_rooms):
            self.rooms.append(Room(slots_per_day))


class Room:
    def __init__(self, slots_per_day):
        self.schedule = Year(SlotType.ROOM, slots_per_day)


class BusinessHours:
    def __init__(self, business_days, opening_hour, closing_hour):
        self.business_days = business_days
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour


class BusinessDays(Enum):
    SEVEN_DAYS = 1
    WEEKDAYS = 2
    NO_SUNDAYS = 3
