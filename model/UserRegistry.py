from model.User import DoctorMapper, PatientMapper, NurseMapper

# TODO add patient_catalog and nurse_catalog


class UserRegistry:
    def __init__(self, tdg):
        self.tdg = tdg
        self.doctor = DoctorMapper(tdg)
        self.patient = PatientMapper(tdg)
        self.nurse = NurseMapper(tdg)
