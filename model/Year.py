from model.Slot import DoctorSlot, RoomSlot
from enum import Enum


class Year:
    def __init__(self, slot_type, slots_per_day):
        # an array of week obj
        self.week = []
        for x in range(0, 54):
            self.week.append(Week(slot_type, slots_per_day))


class Week:
    def __init__(self, slot_type, slots_per_day):
        # an array of day obj
        self.day = []
        for x in range(0, 7):
            self.day.append(Day(slot_type, slots_per_day))


class Day:
    def __init__(self, slot_type, slots_per_day):
        # an array of ** 36 x 20 mins ** slot obj
        self.slot = []
        if slot_type is SlotType.ROOM:
            for x in range(0, slots_per_day):
                self.slot.append(RoomSlot())
        elif slot_type is SlotType.DOCTOR:
            for x in range(0, slots_per_day):
                self.slot.append(DoctorSlot())


class SlotType(Enum):
    ROOM = 1
    DOCTOR = 2
