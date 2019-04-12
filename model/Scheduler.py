from datetime import datetime, timedelta
from typing import Tuple, Union
from model import Clinic
from model.AvailabilityStrategy import WalkInAvailabilityStrategyFactory, AnnualAvailabilityStrategyFactory, \
    RoomAvailabilityStrategy, DoctorAvailabilityStrategy, AvailabilityStrategyFactory
from model.Clinic import Room
from model.Tools import Tools
from model.User import Doctor


class Scheduler:
    # walk-in appointment duration in minutes
    WALK_IN_DURATION = 20

    def __init__(self, mediator):
        self.mediator = mediator

    def find_availability(self, clinic_id: int, date_time: datetime, walk_in: bool):
        if clinic_id is None or date_time is None or walk_in is None:
            return None

        clinic = self.mediator.get_clinic_by_id(clinic_id)
        closing_time = clinic.business_hours.closing_time

        # check if week start is earlier than current week, if not, adjust start time to clinic business hours
        week_start = self.__get_week_start(clinic, date_time)

        if week_start is None:
            return None

        availability_strategy_factory = self.__get_availability_strategy_factory(walk_in)
        room_availability_strategy = availability_strategy_factory.make_room_strategy()
        doctor_availability_strategy = availability_strategy_factory.make_doctor_strategy()

        available_date_times = []
        for day in range(0, 7):
            current_date_time = week_start + timedelta(days=day)
            while current_date_time.time() < closing_time:
                room_available = self.__check_room_availabilities(clinic, current_date_time, closing_time, room_availability_strategy)
                if room_available:
                    doctor_available = self.__check_doctor_availabilities(clinic, current_date_time, doctor_availability_strategy)
                    if doctor_available:
                        available_date_times.append(current_date_time)
                current_date_time += timedelta(minutes=20)

        # now we need to make our availablities into a format valid for fullcalendar
        return Tools.json_from_available_slots(available_date_times, walk_in)

    def confirm_availability(self, clinic_id: int, date_time: datetime, walk_in: bool) -> Union[Tuple[Room, Doctor], None]:
        # final check for appointment time expiration
        if date_time < datetime.now():
            return None

        # step 1: get clinic
        clinic = self.mediator.get_clinic_by_id(clinic_id)

        availability_strategy_factory = self.__get_availability_strategy_factory(walk_in)
        room_availability_strategy = availability_strategy_factory.make_room_strategy()
        doctor_availability_strategy = availability_strategy_factory.make_doctor_strategy()

        room = self.__get_available_room(clinic, date_time, room_availability_strategy)
        if room is not None:
            doctor = self.__get_available_doctor(clinic, date_time, doctor_availability_strategy)
            if doctor is not None:
                return room, doctor
        return None

    def __get_week_start(self, clinic: Clinic, date_time: datetime) -> Union[datetime, None]:
        week_start = date_time.date()
        weekday = week_start.weekday()  # Monday is 0 and Sunday is 6
        if weekday is not 0:
            week_start = week_start - timedelta(days=weekday)  # Go to Monday of week
        hour = clinic.business_hours.opening_time.hour
        minute = clinic.business_hours.opening_time.minute
        # check if this week is in the past
        earliest_time_for_current_week = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 0, 0)
        earliest_time_for_current_week = earliest_time_for_current_week - timedelta(days=earliest_time_for_current_week.weekday())
        if week_start < earliest_time_for_current_week.date():
            return None
        return datetime(week_start.year, week_start.month, week_start.day, hour, minute)

    def __check_room_availabilities(self, clinic: Clinic, date_time: datetime, closing_time: datetime.time, strategy: RoomAvailabilityStrategy) -> bool:
        for room in clinic.rooms.values():
            if strategy.get_availability(room, date_time, closing_time) is not None:
                return True
        return False

    def __check_doctor_availabilities(self, clinic: Clinic, date_time: datetime, strategy: DoctorAvailabilityStrategy) -> bool:
        for doctor in clinic.doctors.values():
            if strategy.get_availability(doctor, date_time) is not None:
                return True
        return False

    def __get_available_room(self, clinic: Clinic, date_time: datetime, strategy: RoomAvailabilityStrategy) -> Union[Room, None]:
        for room in clinic.rooms.values():
            if strategy.get_availability(room, date_time, clinic.business_hours.closing_time) is not None:
                return room
        return None

    def __get_available_doctor(self, clinic: Clinic, date_time: datetime, strategy: DoctorAvailabilityStrategy) -> Union[Doctor, None]:
        for doctor in clinic.doctors.values():
            if strategy.get_availability(doctor, date_time) is not None:
                return doctor
        return None

    def __get_availability_strategy_factory(self, walk_in: bool) -> AvailabilityStrategyFactory:
        if walk_in:
            return WalkInAvailabilityStrategyFactory()
        else:
            return AnnualAvailabilityStrategyFactory()