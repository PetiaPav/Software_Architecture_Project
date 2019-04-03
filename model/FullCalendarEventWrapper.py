from datetime import datetime


class WrapDoctorEvent():
    def __init__(self, fullcalendar_event):
        self.day = self.convert_fullcalendar_day(fullcalendar_event['day'])

        self.walk_in = self.convert_fullcalendar_Walk_in(fullcalendar_event['title'])

    def convert_fullcalendar_day(self, fullcalenday_day):
        fullcalenday_day = int(fullcalenday_day)
        fullcalenday_day = 6 if fullcalenday_day == 0 else fullcalenday_day - 1
        return fullcalenday_day

    def convert_fullcalendar_Walk_in(self, fullcalendar_Walkin):
        return True if fullcalendar_Walkin == 'Walk-in' else False


class WrapDoctorGenericEvent(WrapDoctorEvent):
    def __init__(self, fullcalendar_event):
        WrapDoctorEvent.__init__(self, fullcalendar_event)
        self.date_time = self.create_generic_week_date_time(fullcalendar_event)

    # Monday is 0, Sunday is 6 generic availabilities are stored in the week of September 30th, 2019
    def create_generic_week_date_time(self, fullcalendar_event):
        if self.day == 0:
            return datetime(2019, 9, 30, int(fullcalendar_event['time'][0:2]), int(fullcalendar_event['time'][3:5]))
        else:
            return datetime(2019, 10, self.day, int(fullcalendar_event['time'][0:2]), int(fullcalendar_event['time'][3:5]))
