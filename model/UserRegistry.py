from model.User import DoctorMapper, PatientMapper

# TODO add patient_catalog and nurse_catalog


class UserRegistry:
    def __init__(self, tdg):
        self.tdg = tdg
        self.doctor = DoctorMapper(tdg)
        self.patientMapper = PatientMapper(tdg)

    def get_patient_by_id(self, patient_id):
        return self.patientMapper.get_by_id(patient_id);