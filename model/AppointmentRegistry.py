from model.Appointment import Appointment


class AppointmentRegistry:
    def __init__(self, clinic_registry):
        self.catalog = []
        self.populate(clinic_registry)

    # TODO
    def populate(self, clinic_registry):
        pass
