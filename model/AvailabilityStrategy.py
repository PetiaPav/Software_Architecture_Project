import abc


class Availability(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_availability(self, context, date_time, walk_in, closing_time):
        pass
