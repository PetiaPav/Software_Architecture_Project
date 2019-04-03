from datetime import datetime, timedelta
from model.Tool import Tools
import random


class Scheduler:
    # walk-in appointment duration in minutes
    WALK_IN_DURATION = 20

    def __init__(self, mediator):
        self.mediator = mediator

    # expects date_time as python datetime object(year, month, day, 24hr, min), any day in the week will work

    def find_availablity(self, clinic_id, date_time, walk_in):
        if clinic_id is None or date_time is None or walk_in is None:
            return None

        clinic = self.mediator.get_clinic_by_id(clinic_id)
        closing_time = clinic.business_hours.closing_time

        week_start = self.__get_week_start(clinic, date_time)

        available_date_times = []
        for day in range(0, 7):
            current_date_time = week_start + timedelta(days=day)
            while current_date_time.time() < closing_time:
                room_available = self.__check_room_availabilities(clinic, current_date_time, walk_in)
                if room_available:
                    doctor_available = self.__check_doctor_availabilities(clinic, current_date_time, walk_in)
                    if doctor_available:
                        available_date_times.append(current_date_time)
                current_date_time += timedelta(minutes=20)

        # now we need to make our availablities into a format valid for fullcalendar
        return Tools.json_from_available_slots(available_date_times, walk_in)

    def confirm_availability(self, clinic_id, date_time, walk_in):
        # step 1: get clinic
        clinic = self.mediator.get_clinic_by_id(clinic_id)

        # step 2: find available room (at random)
        room_list = list(clinic.rooms)
        doctor_list = list(clinic.doctors)
        for room in random.sample(range(len(room_list)), len(room_list)):
            if room_list[room].confirm_availability(date_time, walk_in) is True:
                # step 3: find available doctor (at random)
                for doctor in random.sample(range(len(doctor_list)), len(doctor_list)):
                    if doctor_list[doctor].confirm_availability(date_time, walk_in) is True:
                        # we return object references so that the appointment registry can add the appointment ids / bookings directly
                        return (room_list[room], doctor_list[doctor])
        return None

    def __get_week_start(self, clinic, date_time) -> datetime:
        week_start = date_time.date
        weekday = week_start.weekday()  # Monday is 0 and Sunday is 6
        if weekday is not 0:
            week_start = week_start - timedelta(days=weekday)  # Go to Monday of week
        hour = clinic.business_hours.opening_time.hour
        minute = clinic.business_hours.opening_time.minute
        return datetime(week_start.year, week_start.month, week_start.day, hour, minute)

    def __check_room_availabilities(self, clinic, date_time: datetime, walk_in: bool) -> bool:
        for room in clinic.rooms.values():
            if room.get_availability(date_time, walk_in) is not None:
                return True
        return False

    def __check_doctor_availabilities(self, clinic, date_time: datetime, walk_in: bool) -> bool:
        for doctor in clinic.doctors.values():
            if doctor.get_availability(date_time, walk_in) is not None:
                return True
        return False
