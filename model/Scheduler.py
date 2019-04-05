from datetime import datetime, timedelta
from typing import Tuple

from model import Clinic
from model.Clinic import Room
from model.Tool import Tools
import random

from model.User import Doctor


class Scheduler:
    # walk-in appointment duration in minutes
    WALK_IN_DURATION = 20

    def __init__(self, mediator):
        self.mediator = mediator

    # expects date_time as python datetime object(year, month, day, 24hr, min), any day in the week will work

    def find_availability(self, clinic_id: int, date_time: datetime, walk_in: bool):
        if clinic_id is None or date_time is None or walk_in is None:
            return None

        clinic = self.mediator.get_clinic_by_id(clinic_id)
        closing_time = clinic.business_hours.closing_time

        week_start = self.__get_week_start(clinic, date_time)

        available_date_times = []
        for day in range(0, 7):
            current_date_time = week_start + timedelta(days=day)
            while current_date_time.time() < closing_time:
                room_available = self.__check_room_availabilities(clinic, current_date_time, walk_in, closing_time)
                if room_available:
                    doctor_available = self.__check_doctor_availabilities(clinic, current_date_time, walk_in)
                    if doctor_available:
                        available_date_times.append(current_date_time)
                current_date_time += timedelta(minutes=20)

        # now we need to make our availablities into a format valid for fullcalendar
        return Tools.json_from_available_slots(available_date_times, walk_in)

    def confirm_availability(self, clinic_id: int, date_time: datetime, walk_in: bool) -> Tuple[Room, Doctor]:
        # step 1: get clinic
        clinic = self.mediator.get_clinic_by_id(clinic_id)

        room = self.__get_available_room(clinic, date_time, walk_in)
        if room is not None:
            doctor = self.__get_available_doctor(clinic, date_time, walk_in)
            if doctor is not None:
                return room, doctor
        return None

    def __get_week_start(self, clinic: Clinic, date_time: datetime) -> datetime:
        week_start = date_time.date()
        weekday = week_start.weekday()  # Monday is 0 and Sunday is 6
        if weekday is not 0:
            week_start = week_start - timedelta(days=weekday)  # Go to Monday of week
        hour = clinic.business_hours.opening_time.hour
        minute = clinic.business_hours.opening_time.minute
        return datetime(week_start.year, week_start.month, week_start.day, hour, minute)

    def __check_room_availabilities(self, clinic: Clinic, date_time: datetime, walk_in: bool, closing_time: datetime.time) -> bool:
        for room in clinic.rooms.values():
            if room.get_availability(date_time, walk_in, closing_time) is not None:
                return True
        return False

    def __check_doctor_availabilities(self, clinic: Clinic, date_time: datetime, walk_in: bool) -> bool:
        for doctor in clinic.doctors.values():
            if doctor.get_availability(date_time, walk_in) is not None:
                return True
        return False

    def __get_available_doctor(self, clinic, date_time: datetime, walk_in: bool):
        for doctor in clinic.doctors.values():
            if doctor.get_availability(date_time, walk_in) is not None:
                return doctor
        return None

    def __get_available_room(self, clinic, date_time: datetime, walk_in: bool):
        for room in clinic.rooms.values():
            if room.get_availability(date_time, walk_in, clinic.business_hours.closing_time) is not None:
                return room
        return None
