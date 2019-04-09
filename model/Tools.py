import json
from datetime import datetime, timedelta


class Tools:
    SLOTS_PER_DAY = 72

    @staticmethod
    def int_to_bool(value):
        if value == 0:
            return False
        else:
            return True

    @staticmethod
    def json_from_available_slots(available_slots, walk_in):
        id_counter = 0
        pydict = []
        # available slots are tuples of (week_index, day_index, slot_index)
        for date_time in available_slots:
            start_time = date_time.strftime("%Y-%m-%dT%H:%M:%S")
            if walk_in:
                end_time = (date_time + timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%S")
            else:
                end_time = (date_time + timedelta(minutes=60)).strftime("%Y-%m-%dT%H:%M:%S")
            pydict.append({
                "id": id_counter,
                "title": 'available',
                "start": start_time,
                "end": end_time
            })
            id_counter += 1
        return json.dumps(pydict)

    @staticmethod
    def json_from_doctor_week_availabilities(availability_dict):
        pydict = []
        counter = 0
        for date_time, walk_in in availability_dict.items():
            counter += 1
            generated_id = "generated_available_" + str(counter)
            start_time = date_time.strftime("%Y-%m-%dT%H:%M:%S")
            if walk_in:
                end_time = (date_time + timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%S")
                event_title = "Walk-in"
            else:
                end_time = (date_time + timedelta(minutes=60)).strftime("%Y-%m-%dT%H:%M:%S")
                event_title = "Annual"
            pydict.append({"title": event_title, "start": start_time, "end": end_time, "id": generated_id})
        return pydict

    @staticmethod
    def json_from_doctor_week_appointments(schedule_dict):
        pydict = []
        counter = 0
        for date_time, walk_in in schedule_dict.items():
            counter += 1
            generated_id = "generated_booked_" + str(counter)
            start_time = date_time.strftime("%Y-%m-%dT%H:%M:%S")
            event_color = "orange"
            if walk_in:
                end_time = (date_time + timedelta(minutes=20)).strftime("%Y-%m-%dT%H:%M:%S")
                event_title = "Walk-in"
            else:
                end_time = (date_time + timedelta(minutes=60)).strftime("%Y-%m-%dT%H:%M:%S")
                event_title = "Annual"
            pydict.append({"title": event_title, "start": start_time, "end": end_time, "color": event_color, "id": generated_id})
        return pydict

    @staticmethod
    def convert_to_python_datetime(fullcalendar_datetime):
        hour = 0
        minute = 0
        if len(fullcalendar_datetime) > len("2019-04-01T00:"):
            hour = int(fullcalendar_datetime[11:13])
            minute = int(fullcalendar_datetime[14:16])
        return datetime(int(fullcalendar_datetime[0:4]), int(fullcalendar_datetime[5:7]), int(fullcalendar_datetime[8:10]), hour, minute)

    @staticmethod
    def convert_to_date_time(input_datetime):
        return datetime.strptime(input_datetime, '%Y-%m-%dT%H:%M:%S')

    @staticmethod
    def get_date_iso_format(input_datetime):
        return input_datetime.date().isoformat()

    @staticmethod
    def get_time_iso_format(input_datetime):
        return input_datetime.time().isoformat()

    @staticmethod
    def get_unavailable_times_message(date_time):
        pylist = []
        week_start = date_time - timedelta(days=date_time.weekday())
        for day in range(0, 7):
            start_time = week_start + timedelta(days=day)
            start_time = datetime(start_time.year, start_time.month, start_time.day, 12, 0)
            end_time = start_time + timedelta(hours=1)
            start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
            end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
            pylist.append({
                "id": "expired",
                "title": "please select a future date",
                "start": start_time,
                "end": end_time,
                "color": "red"
            })
        return json.dumps(pylist)
