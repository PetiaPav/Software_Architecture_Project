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
            return

        # step 1: get clinic
        clinic = self.mediator.get_clinic_by_id(clinic_id)

        # step 2: build room_truth_table
        # 2.1 get week / day start and end time from date_time and clinic business hours
        week_start = self.__get_week_start(clinic, date_time)
        week_end = self.__get_week_end(clinic, week_start)


        # step 3: build list of times to check for rooms and doctors
        current_date_time = week_start
        for day in range(1,8):
            while current_day_start_time < current_day_end_time:
                # truth tables of tupples (boolean = room/doctor availability, datetime = time of current availablity)
                room_truth_table.append((False, current_day_start_time))
                doctor_truth_table.append((False, current_day_start_time))
                current_day_start_time = current_day_end_time + timedelta(minutes=Scheduler.WALK_IN_DURATION)

            current_date_time = week_start + timedelta(days=day)

        # step 4: send the room_truth_table to every room in the clinic
        if walk_in is True:
            for room in clinic.rooms.values():
                room_truth_table = room.get_week_availability_walk_in(room_truth_table)
        else:
            for room in clinic.rooms.values():
                room_truth_table = room.get_week_availability_annual(room_truth_table)

        # step 5: send the doctor_truth_table to every doctor in the clinic
        if walk_in is True:
            for doctor in clinic.doctors.values():
                doctor_truth_table = doctor.get_week_availability_walk_in(doctor_truth_table)
        else:
            for doctor in clinic.doctors.values():
                doctor_truth_table = doctor.get_week_availability_annual(doctor_truth_table)

        # step 6: AND the truth tables to determine actual availabilities
        available_slots = []
        for truth_table_iterator in room_truth_table:
            if room_truth_table[truth_table_iterator][0] is True and doctor_truth_table[truth_table_iterator][0] is True:
                available_slots.append(room_truth_table[truth_table_iterator][1])

        # now we need to make our availablities into a format valid for fullcalendar
        return Tools.json_from_available_slots(available_slots, walk_in)

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

    def __get_week_start(self, clinic, date_time):
        week_start = date_time.date
        weekday = week_start.weekday()  # Monday is 0 and Sunday is 6
        if weekday is not 0:
            week_start = week_start - timedelta(days=weekday)  # Go to Monday of week
        hour = clinic.business_hours.opening_time.hour
        minute = clinic.business_hours.opening_time.minute
        return datetime(week_start.year, week_start.month, week_start.day, hour, minute)

    def __get_week_end(self, clinic, week_start):
        hour = clinic.business_hours.closing_time.hour
        minute = clinic.business_hours.closing_time.minute

        return datetime(week_start.year, week_start.month, week_start.day, hour, minute) + timedelta(days=6)

