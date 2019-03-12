import json


week_dict = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}


time_dict = {
    0: "00:00",
    1: "00:20",
    2: "00:40",
    3: "01:00",
    4: "01:20",
    5: "01:40",
    6: "02:00",
    7: "02:20",
    8: "02:40",
    9: "03:00",
    10: "03:20",
    11: "03:40",
    12: "04:00",
    13: "04:20",
    14: "04:40",
    15: "05:00",
    16: "05:20",
    17: "05:40",
    18: "06:00",
    19: "06:20",
    20: "06:40",
    21: "07:00",
    22: "07:20",
    23: "07:40",
    24: "08:00",
    25: "08:20",
    26: "08:40",
    27: "09:00",
    28: "09:20",
    29: "09:40",
    30: "10:00",
    31: "10:20",
    32: "10:40",
    33: "11:00",
    34: "11:20",
    35: "11:40",
    36: "12:00",
    37: "12:20",
    38: "12:40",
    39: "13:00",
    40: "13:20",
    41: "13:40",
    42: "14:00",
    43: "14:20",
    44: "14:40",
    45: "15:00",
    46: "15:20",
    47: "15:40",
    48: "16:00",
    49: "16:20",
    50: "16:40",
    51: "17:00",
    52: "17:20",
    53: "17:40",
    54: "18:00",
    55: "18:20",
    56: "18:40",
    57: "19:00",
    58: "19:20",
    59: "19:40",
    60: "20:00",
    61: "20:20",
    62: "20:40",
    63: "21:00",
    64: "21:20",
    65: "21:40",
    66: "22:00",
    67: "22:20",
    68: "22:40",
    69: "23:00",
    70: "23:20",
    71: "23:40",
    72: "00:00"
}

# TODO write method to generate dict for a given year

year_2019_dict = {
    0: [None, None, "01-01", "01-02", "01-03", "01-04", "01-05"],
    1: ["01-06", "01-07", "01-08", "01-09", "01-10", "01-11", "01-12"],
    2: ["01-13", "01-14", "01-15", "01-16", "01-17", "01-18", "01-19"],
    3: ["01-20", "01-21", "01-22", "01-23", "01-24", "01-25", "01-26"],
    4: ["01-27", "01-28", "01-29", "01-30", "01-31", "02-01", "02-02"],
    5: ["02-03", "02-04", "02-05", "02-06", "02-07", "02-08", "02-09"],
    6: ["02-10", "02-11", "02-12", "02-13", "02-14", "02-15", "02-16"],
    7: ["02-17", "02-18", "02-19", "02-20", "02-21", "02-22", "02-23"],
    8: ["02-24", "02-25", "02-26", "02-27", "02-28", "03-01", "03-02"],
    9: ["03-03", "03-04", "03-05", "03-06", "03-07", "03-08", "03-09"],
    10: ["03-10", "03-11", "03-12", "03-13", "03-14", "03-15", "03-16"],
    11: ["03-17", "03-18", "03-19", "03-20", "03-21", "03-22", "03-23"],
    12: ["03-24", "03-25", "03-26", "03-27", "03-28", "03-29", "03-30"],
    13: ["03-31", "04-01", "04-02", "04-03", "04-04", "04-05", "04-06"],
    14: ["04-07", "04-08", "04-09", "04-10", "04-11", "04-12", "04-13"],
    15: ["04-14", "04-15", "04-16", "04-17", "04-18", "04-19", "04-20"],
    16: ["04-21", "04-22", "04-23", "04-24", "04-25", "04-26", "04-27"],
    17: ["04-28", "04-29", "04-30", "05-01", "05-02", "05-03", "05-04"],
    18: ["05-05", "05-06", "05-07", "05-08", "05-09", "05-10", "05-11"],
    19: ["05-12", "05-13", "05-14", "05-15", "05-16", "05-17", "05-18"],
    20: ["05-19", "05-20", "05-21", "05-22", "05-23", "05-24", "05-25"],
    21: ["05-26", "05-27", "05-28", "05-29", "05-30", "05-31", "06-01"],
    22: ["06-02", "06-03", "06-04", "06-05", "06-06", "06-07", "06-08"],
    23: ["06-09", "06-10", "06-11", "06-12", "06-13", "06-14", "06-15"],
    24: ["06-16", "06-17", "06-18", "06-19", "06-20", "06-21", "06-22"],
    25: ["06-23", "06-24", "06-25", "06-26", "06-27", "06-28", "06-29"],
    26: ["06-30", "07-01", "07-02", "07-03", "07-04", "07-05", "07-06"],
    27: ["07-07", "07-08", "07-09", "07-10", "07-11", "07-12", "07-13"],
    28: ["07-14", "07-15", "07-16", "07-17", "07-18", "07-19", "07-20"],
    29: ["07-21", "07-22", "07-23", "07-24", "07-25", "07-26", "07-27"],
    30: ["07-28", "07-29", "07-30", "07-31", "08-01", "08-02", "08-03"],
    31: ["08-04", "08-05", "08-06", "08-07", "08-08", "08-09", "08-10"],
    32: ["08-11", "08-12", "08-13", "08-14", "08-15", "08-16", "08-17"],
    33: ["08-18", "08-19", "08-20", "08-21", "08-22", "08-23", "08-24"],
    34: ["08-25", "08-26", "08-27", "08-28", "08-29", "08-30", "08-31"],
    35: ["09-01", "09-02", "09-03", "09-04", "09-05", "09-06", "09-07"],
    36: ["09-08", "09-09", "09-10", "09-11", "09-12", "09-13", "09-14"],
    37: ["09-15", "09-16", "09-17", "09-18", "09-19", "09-20", "09-21"],
    38: ["09-22", "09-23", "09-24", "09-25", "09-26", "09-27", "09-28"],
    39: ["09-29", "09-30", "10-01", "10-02", "10-03", "10-04", "10-05"],
    40: ["10-06", "10-07", "10-08", "10-09", "10-10", "10-11", "10-12"],
    41: ["10-13", "10-14", "10-15", "10-16", "10-17", "10-18", "10-19"],
    42: ["10-20", "10-21", "10-22", "10-23", "10-24", "10-25", "10-26"],
    43: ["10-27", "10-28", "10-29", "10-30", "10-31", "11-01", "11-02"],
    44: ["11-03", "11-04", "11-05", "11-06", "11-07", "11-08", "11-09"],
    45: ["11-10", "11-11", "11-12", "11-13", "11-14", "11-15", "11-16"],
    46: ["11-17", "11-18", "11-19", "11-20", "11-21", "11-22", "11-23"],
    47: ["11-24", "11-25", "11-26", "11-27", "11-28", "11-29", "11-30"],
    48: ["12-01", "12-02", "12-03", "12-04", "12-05", "12-06", "12-07"],
    49: ["12-08", "12-09", "12-10", "12-11", "12-12", "12-13", "12-14"],
    50: ["12-15", "12-16", "12-17", "12-18", "12-19", "12-20", "12-21"],
    51: ["12-22", "12-23", "12-24", "12-25", "12-26", "12-27", "12-28"],
    52: ["12-29", "12-30", "12-31", None, None, None, None],
    53: [None, None, None, None, None, None, None]
}


class Tools:
    SLOTS_PER_DAY = 72

    @staticmethod
    def get_day_string_from_day_index(index):
        return week_dict[index]

    @staticmethod
    def get_time_string_from_slot_index(index):
        return time_dict[index]

    @staticmethod
    def get_week_and_day_index_from_date(yyyy_mm_dd):
        day_index = None
        for week_index, day_list in eval("year_" + yyyy_mm_dd[0:4] + "_dict").items():
            for date in day_list:
                if date == yyyy_mm_dd[5:10]:
                    day_index = day_list.index(date)
                    return (week_index, day_index)
        return None

    # expects date_time format as string: "2019-01-27T08:00:00"
    @staticmethod
    def get_week_index_from_date(date_time):
        for week_index, day_list in eval("year_" + date_time[0:4] + "_dict").items():
            for date in day_list:
                if date == date_time[5:10]:
                    return week_index
        return None

    @staticmethod
    def get_slot_index_from_time(time_24h_string):
        for key in time_dict:
            if time_dict[key] == time_24h_string:
                return int(key)
        return None

    @staticmethod
    def int_to_24hr_format(int_hour):
        if int_hour < 10:
            return "0" + str(int_hour) + ':00'
        else:
            return str(int_hour) + ':00'

    @staticmethod
    def get_date_time_from_slot_yearly_index(slot_yearly_index):
        week_index = int(slot_yearly_index / (Tools.SLOTS_PER_DAY * 7))
        day_index = int((slot_yearly_index % (Tools.SLOTS_PER_DAY * 7)) / Tools.SLOTS_PER_DAY)
        slot_index = slot_yearly_index % Tools.SLOTS_PER_DAY
        return "2019-" + year_2019_dict[week_index][day_index] + "T" + time_dict[slot_index] + ":00"

    @staticmethod
    def get_slot_index_from_slot_yearly_index(slot_yearly_index):
        return slot_yearly_index % Tools.SLOTS_PER_DAY

    @staticmethod
    def get_slot_yearly_index_from_week_day_slot(week_index, day_index, slot_index):
        return week_index * Tools.SLOTS_PER_DAY * 7 + day_index * Tools.SLOTS_PER_DAY + slot_index

    @staticmethod
    def get_week_index_from_slot_yearly_index(slot_yearly_index):
        return int(slot_yearly_index / (Tools.SLOTS_PER_DAY * 7))

    @staticmethod
    def get_day_index_from_slot_yearly_index(slot_yearly_index):
        return int((slot_yearly_index % (Tools.SLOTS_PER_DAY * 7)) / Tools.SLOTS_PER_DAY)

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
        for tup in available_slots:
            start_time = "2019-" + year_2019_dict[tup[0]][tup[1]] + "T" + time_dict[tup[2]] + ":00"
            if walk_in:
                end_time = "2019-" + year_2019_dict[tup[0]][tup[1]] + "T" + time_dict[tup[2]+1] + ":00"
            else:
                end_time = "2019-" + year_2019_dict[tup[0]][tup[1]] + "T" + time_dict[tup[2]+3] + ":00"
            pydict.append({
                "id": id_counter,
                "title": 'available',
                "start": start_time,
                "end": end_time
            })
            id_counter += 1
        return json.dumps(pydict)

    @staticmethod
    def json_from_available_slots_doctor_available(availability_list):
        pydict = []
        counter = 0
        for availability in availability_list:
            counter += 1
            generated_id = "generated_available_" + str(counter)
            available_slot = availability[0]
            walk_in = availability[1]

            start_time = "2019-" + year_2019_dict[available_slot[0]][available_slot[1]] + "T" + time_dict[available_slot[2]] + ":00"
            if walk_in:
                end_time = "2019-" + year_2019_dict[available_slot[0]][available_slot[1]] + "T" + time_dict[available_slot[2] + 1] + ":00"
                event_title = "Walk-in"
            else:
                end_time = "2019-" + year_2019_dict[available_slot[0]][available_slot[1]] + "T" + time_dict[available_slot[2] + 3] + ":00"
                event_title = "Annual"
            pydict.append({"title": event_title, "start": start_time, "end": end_time, "id": generated_id})
        return pydict

    @staticmethod
    def json_from_available_slots_doctor_scheduled(availability_list):
        pydict = []
        counter = 0
        for availability in availability_list:
            counter += 1
            generated_id = "generated_booked_" + str(counter)
            available_slot = availability[0]
            walk_in = availability[1]
            
            start_time = "2019-" + year_2019_dict[available_slot[0]][available_slot[1]] + "T" + time_dict[available_slot[2]] + ":00"
            if walk_in:
                end_time = "2019-" + year_2019_dict[available_slot[0]][available_slot[1]] + "T" + time_dict[available_slot[2] + 1] + ":00"
                event_title = "Walk-in"
                event_color = "orange"
            else:
                end_time = "2019-" + year_2019_dict[available_slot[0]][available_slot[1]] + "T" + time_dict[available_slot[2] + 3] + ":00"
                event_title = "Annual"
                event_color = "orange"
            pydict.append({"title": event_title, "start": start_time, "end": end_time, "color": event_color, "id": generated_id})
        return pydict
