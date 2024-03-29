from model.User import DoctorMapper, PatientMapper, NurseMapper


class UserRegistry:

    __instance_of_registry = None

    def __init__(self, mediator, tdg):
        self.tdg = tdg
        self.doctor = DoctorMapper(mediator, tdg)
        self.patient = PatientMapper(mediator, tdg)
        self.nurse = NurseMapper(tdg)

    @staticmethod
    def get_instance(mediator, tdg):
        if UserRegistry.__instance_of_registry is None:
            UserRegistry.__instance_of_registry = UserRegistry(mediator, tdg)
        return UserRegistry.__instance_of_registry
