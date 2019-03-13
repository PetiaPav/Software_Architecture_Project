from model.User import DoctorMapper, PatientMapper, NurseMapper


class UserRegistry:
    
    __instance_of_registry = None

    def __init__(self, tdg):
        self.tdg = tdg
        self.doctor = DoctorMapper(tdg)
        self.patient = PatientMapper(tdg)
        self.nurse = NurseMapper(tdg)

    @staticmethod
    def get_instance(tdg):
        if UserRegistry.__instance_of_registry is None:
            UserRegistry.__instance_of_registry = UserRegistry(tdg)
        return UserRegistry.__instance_of_registry
