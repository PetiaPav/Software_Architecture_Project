from model.User import DoctorMapper

# TODO add patient_catalog and nurse_catalog


class UserRegistry:
    def __init__(self, tdg):
        self.tdg = tdg
        self.doctor = DoctorMapper(tdg)
