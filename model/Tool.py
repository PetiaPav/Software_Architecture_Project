import json
from datetime import datetime


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
