from model.Slot import DoctorSlot, RoomSlot
from enum import Enum


class Year:

    # based on 24 hours per day, 3 slots (20 minute slots) per hour
    SLOTS_PER_DAY = 72 

    def __init__(self, slot_type):
        # an array of week obj
        self.week = []
        for x in range(0, 54):
            self.week.append(Week(slot_type))


class Week:
    def __init__(self, slot_type):
        # an array of day obj
        self.day = []
        for x in range(0, 7):
            self.day.append(Day(slot_type))


class Day:
    def __init__(self, slot_type):
        self.slot = []
        if slot_type is SlotType.ROOM:
            for x in range(0, Year.SLOTS_PER_DAY):
                self.slot.append(RoomSlot())
        elif slot_type is SlotType.DOCTOR:
            for x in range(0, Year.SLOTS_PER_DAY):
                self.slot.append(DoctorSlot())


class SlotType(Enum):
    ROOM = 1
    DOCTOR = 2
