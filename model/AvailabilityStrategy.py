import abc
from datetime import timedelta, datetime

from model.Clinic import Room
from model.User import Doctor


class AvailabilityStrategyFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def make_room_strategy(self):
        pass

    @abc.abstractmethod
    def make_doctor_strategy(self):
        pass


class WalkInAvailabilityStrategyFactory(AvailabilityStrategyFactory):
    def make_room_strategy(self):
        return WalkInRoomAvailabilityStrategy()

    def make_doctor_strategy(self):
        return WalkInDoctorAvailabilityStrategy()


class AnnualAvailabilityStrategyFactory(AvailabilityStrategyFactory):
    def make_room_strategy(self):
        return AnnualRoomAvailabilityStrategy()

    def make_doctor_strategy(self):
        return AnnualDoctorAvailabilityStrategy()


class DoctorAvailabilityStrategy(metaclass=abc.ABCMeta):

    def get_availability(self, doctor: Doctor, date_time: datetime):
        pass


class WalkInDoctorAvailabilityStrategy(DoctorAvailabilityStrategy):

    def get_availability(self, doctor: Doctor, date_time: datetime):
        if date_time < datetime.now() or date_time in doctor.appointment_dict:
            return None

        for adjustment in doctor.adjustment_list:
            if adjustment.date_time == date_time:
                if adjustment.operation_type_add:
                    if adjustment.walk_in:
                        return doctor
                else:
                    return None

        generic_day_availability = doctor.generic_week_availability[date_time.weekday()]
        try:
            if generic_day_availability[date_time.time()]:
                return doctor
            else:
                return None
        except KeyError:
            return None


class AnnualDoctorAvailabilityStrategy(DoctorAvailabilityStrategy):

    def get_availability(self, doctor: Doctor, date_time: datetime):
        if date_time < datetime.now() or date_time in doctor.appointment_dict:
            return None

        for adjustment in doctor.adjustment_list:
            if adjustment.date_time == date_time:
                if adjustment.operation_type_add:
                    if not adjustment.walk_in:
                        return doctor
                else:
                    return None

        generic_day_availability = doctor.generic_week_availability[date_time.weekday()]
        try:
            if not generic_day_availability[date_time.time()]:
                return doctor
            else:
                return None
        except KeyError:
            return None


class RoomAvailabilityStrategy(metaclass=abc.ABCMeta):

    def get_availability(self, room: Room, date_time: datetime, closing_time: datetime.time):
        pass


class WalkInRoomAvailabilityStrategy(RoomAvailabilityStrategy):

    def get_availability(self, room: Room, date_time: datetime, closing_time: datetime.time):
        date_time_to_check = date_time
        if date_time_to_check in room.bookings_dict:  # Checking the requested time
            return None

        #  Checking if there are annual appointments in the previous two slots
        date_time_to_check -= timedelta(minutes=20)
        if date_time_to_check in room.bookings_dict:
            if room.bookings_dict[date_time_to_check] is False:
                return None
        else:
            date_time_to_check -= timedelta(minutes=20)
            if date_time_to_check in room.bookings_dict and room.bookings_dict[date_time_to_check] is False:
                return None
        return self


class AnnualRoomAvailabilityStrategy(RoomAvailabilityStrategy):

    def get_availability(self, room: Room, date_time: datetime, closing_time: datetime.time):
        date_time_to_check = date_time
        if date_time_to_check in room.bookings_dict:  # Checking the requested time
            return None

            #  Checking if there are annual appointments in the previous two slots
        date_time_to_check -= timedelta(minutes=20)
        if date_time_to_check in room.bookings_dict:
            if room.bookings_dict[date_time_to_check] is False:
                return None
        else:
            date_time_to_check -= timedelta(minutes=20)
            if date_time_to_check in room.bookings_dict and room.bookings_dict[date_time_to_check] is False:
                return None

        date_time_to_check = date_time + timedelta(minutes=40)
        if date_time_to_check.time() >= closing_time:
            return None

        date_time_to_check = date_time + timedelta(minutes=20)
        if date_time_to_check in room.bookings_dict:
            return None
        date_time_to_check += timedelta(minutes=20)
        if date_time_to_check in room.bookings_dict:
            return None

        return self
