from model.Tdg import Tdg



class UserMapper:
    def __init__(self, app):
        self.tdg = Tdg(app)

    def get_patient_by_id(self, id):
        patient_data = self.tdg.get_patient_by_id(id)
        user_data = self.tdg.get_user_by_id(patient_data["user_fk"])
        patient = {}

        patient["id"] = patient_data["id"]
        patient["email"] = patient_data["email"]
        patient["health_card"] = patient_data["health_card"]
        patient["phone_number"] = patient_data["phone_number"]
        patient["birthday"] = patient_data["birthday"]
        patient["gender"] = patient_data["gender"]
        patient["physical_address"] = patient_data["physical_address"]
        patient["first_name"] = user_data["first_name"]
        patient["last_name"] = user_data["last_name"]

        return patient