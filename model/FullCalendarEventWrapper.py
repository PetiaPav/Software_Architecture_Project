from datetime import datetime
from model.Tools import Tools


class WrapDoctorEvent():
    def __init__(self, fullcalendar_event):
        self.day = self.convert_fullcalendar_day(fullcalendar_event['day'])

        self.walk_in = self.convert_fullcalendar_Walk_in(fullcalendar_event['title'])

    def convert_fullcalendar_day(self, fullcalendar_day):
        fullcalendar_day = int(fullcalendar_day)
        fullcalendar_day = 6 if fullcalendar_day == 0 else fullcalendar_day - 1
        return fullcalendar_day

    def convert_fullcalendar_Walk_in(self, fullcalendar_Walkin):
        return True if fullcalendar_Walkin == 'Walk-in' else False


class WrapDoctorGenericEvent(WrapDoctorEvent):
    def __init__(self, fullcalendar_event):
        WrapDoctorEvent.__init__(self, fullcalendar_event)
        self.time = self.create_generic_week_date_time(fullcalendar_event)

    # Monday is 0, Sunday is 6 generic availabilities are stored in the week of September 30th, 2019
    def create_generic_week_date_time(self, fullcalendar_event):
            return datetime(2019, 1, 1, int(fullcalendar_event['time'][0:2]), int(fullcalendar_event['time'][3:5])).time()


class WrapDoctorAdjustmentEvent(WrapDoctorEvent):
    def __init__(self, fullcalendar_event):
        WrapDoctorEvent.__init__(self, fullcalendar_event)
        self.date_time = Tools.convert_to_python_datetime(fullcalendar_event['time'])
        self.operation_type_add = self.convert_id_to_operation_type(fullcalendar_event['id'])

    def convert_id_to_operation_type(self, fullcalendar_id):
        return True if fullcalendar_id == 'new-availability' else False
