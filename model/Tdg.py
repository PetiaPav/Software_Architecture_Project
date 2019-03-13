from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


class Tdg:
    def __init__(self, app, db_env):
        self.mysql = MySQL(cursorclass=DictCursor)

        # Config MySQL
        app.config['MYSQL_DATABASE_USER'] = 'soen344'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'ubersante'
        app.config['MYSQL_DATABASE_DB'] = db_env
        app.config['MYSQL_DATABASE_HOST'] = 'mydbinst.ccaem9daeat5.us-east-2.rds.amazonaws.com'

        # init MYSQL
        self.mysql.init_app(app)

    def insert_patient(self, email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address):
        connection = self.mysql.connect()
        cur = connection.cursor()

        cur.execute("INSERT INTO USERS(id, first_name, last_name, password) VALUES (NULL, %s, %s, %s)",
                    (first_name, last_name, password))
        last_inserted_id = cur.lastrowid

        cur.execute("INSERT INTO PATIENTS(id, user_fk, email, health_card, phone_number, birthday, gender, physical_address) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s)",
                    (last_inserted_id, email, health_card, phone_number, birthday, gender, physical_address))

        cur.close()
        connection.commit()

    def insert_doctor(self, first_name, last_name, password, permit_number, specialty, city):
        connection = self.mysql.connect()
        cur = connection.cursor()

        cur.execute("INSERT INTO USERS(id, first_name, last_name, password) VALUES (NULL, %s, %s, %s)",
                    (first_name, last_name, password))
        last_inserted_id = cur.lastrowid

        cur.execute("INSERT INTO DOCTORS(id, user_fk, permit_number, specialty, city) VALUES(NULL, %s, %s, %s, %s)",
                    (last_inserted_id, permit_number, specialty, city))

        cur.close()
        connection.commit()

    def insert_nurse(self, first_name, last_name, password, access_id):
        connection = self.mysql.connect()
        cur = connection.cursor()

        cur.execute("INSERT INTO USERS(id, first_name, last_name, password) VALUES (NULL, %s, %s, %s)",
                    (first_name, last_name, password))
        last_inserted_id = cur.lastrowid

        cur.execute("INSERT INTO NURSES(id, user_fk, access_id) VALUES(NULL, %s, %s)", (last_inserted_id, access_id))

        cur.close()
        connection.commit()

    def get_patient_by_email(self, email):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM PATIENTS WHERE email =%s", [email])
        user_data = cur.fetchone()
        if user_data is None:
            return False
        cur.execute("SELECT * FROM USERS WHERE id =%s", [user_data["user_fk"]])
        patient_data = cur.fetchone()
        cur.close()
        patient_data.update(user_data)
        return patient_data

    def get_nurse_by_access_id(self, access_id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM NURSES WHERE access_id =%s", [access_id])
        user_data = cur.fetchone()
        if user_data is None:
            return False
        cur.execute("SELECT * FROM USERS WHERE id =%s", [user_data["user_fk"]])
        nurse_data = cur.fetchone()
        cur.close()
        nurse_data.update(user_data)
        return nurse_data

    def get_all_patients(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM PATIENTS LEFT JOIN USERS USR ON (PATIENTS.user_fk = USR.id)")
        all_patients = []
        for patient in cur:
            all_patients.append(patient)
        cur.close()
        return all_patients

    def get_all_nurses(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM NURSES LEFT JOIN USERS USR ON (NURSES.user_fk = USR.id)")
        all_nurses = []
        for nurse in cur:
            all_nurses.append(nurse)
        cur.close()
        return all_nurses

    def get_all_doctors(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM DOCTORS LEFT JOIN USERS USR ON (DOCTORS.user_fk = USR.id)")
        doctors = []
        for doctor in cur:
            doctors.append(doctor)
        cur.close()
        return doctors

    def update_doctor_availability(self, doctor_id, list_of_availabilities):
        connection = self.mysql.connect()
        cur = connection.cursor()
        # delete all existing availability for this doctor
        cur.execute("DELETE FROM DOCTOR_AVAILABILITIES WHERE doctor_id=%s", [doctor_id])
        # populate new availability
        for avail in list_of_availabilities:
            cur.execute("INSERT INTO DOCTOR_AVAILABILITIES (id, doctor_id, day_index, slot_index, walk_in) VALUES (NULL, %s, %s, %s, %s)", (avail['doctor_id'], avail['day'], avail['slot_index'], avail['walk_in']))
        connection.commit()
        cur.close()

    def get_doctor_availabilities(self, doctor_id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM DOCTOR_AVAILABILITIES WHERE doctor_id=%s", [doctor_id])
        doctor_availabilities = []
        for availabilities in cur:
            doctor_availabilities.append(availabilities)
        cur.close()
        return doctor_availabilities

    def update_doctor_availabilities_special(self, doctor_id, list_for_tdg, list_of_ids_to_delete):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for id_to_delete in list_of_ids_to_delete:
            cur.execute("DELETE FROM DOCTOR_AVAILABILITIES_SPECIAL WHERE id=%s", [id_to_delete])
        for special_availability in list_for_tdg:
            cur.execute("INSERT INTO DOCTOR_AVAILABILITIES_SPECIAL (id, doctor_id, week_index, day_index, slot_index, walk_in, available) VALUES (NULL, %s, %s, %s, %s, %s, %s)", (doctor_id, special_availability.week_index, special_availability.day_index, special_availability.slot_index, special_availability.walk_in, special_availability.available))
        connection.commit()
        cur.close()

    def get_doctor_availabilities_special(self, doctor_id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM DOCTOR_AVAILABILITIES_SPECIAL WHERE doctor_id=%s", [doctor_id])
        doctor_availabilities_special = []
        for availabilities_special in cur:
            doctor_availabilities_special.append(availabilities_special)
        cur.close()
        return doctor_availabilities_special

    def get_patient_by_id(self, id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM PATIENTS LEFT JOIN USERS USR ON (PATIENTS.user_fk = USR.id WHERE id =%s",
                             [id])
        patient_data = cur.fetchone()
        cur.close()
        if result is None:
            return False
        else:
            return patient_data

    def get_doctor_by_permit_number(self, permit_number):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM DOCTORS WHERE permit_number =%s", [permit_number])
        user_data = cur.fetchone()
        if user_data is None:
            return False
        cur.execute("SELECT * FROM USERS WHERE id =%s", [user_data["user_fk"]])
        doctor_data = cur.fetchone()
        cur.close()
        doctor_data.update(user_data)
        return doctor_data

    def get_all_users(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        users = []
        cur.execute("SELECT * FROM USERS")
        for row in cur.fetchall():
            users.append(row)
        if users is None:
            return False
        cur.close()
        return users

    def get_user_by_id(self, id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM USERS WHERE id =%s", [id])
        user_data = cur.fetchone()
        cur.close()
        if result is None:
            return False
        else:
            return user_data

    def get_clinics(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM CLINICS")
        clinics = []
        for clinic in cur:
            clinics.append(clinic)
        cur.close()
        return clinics

    def get_all_doctor_clinic_assignments(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM DOCTOR_CLINIC_ASSIGNMENT")
        clinic_doctor_assignments = []
        for clinic_doctor_assignment in cur:
            clinic_doctor_assignments.append(clinic_doctor_assignment)
        cur.close()
        return clinic_doctor_assignments

    def get_room_slots_by_clinic_id(self, clinic_id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM ROOM_SLOTS WHERE clinic_id=%s", [clinic_id])
        room_slots = []
        for room_slot in cur:
            room_slots.append(room_slot)
        cur.close()
        if len(room_slots) > 0:
            return room_slots
        else:
            return None

    def update_room_slot(self, room_slot):
        connection = self.mysql.connect()
        cur = connection.cursor()
        if room_slot.id is None:
            cur.execute("INSERT INTO ROOM_SLOTS (id, room_id, slot_id, walk_in, doctor_id, patient_id) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s)", (room_slot.room_id, room_slot.slot_yearly_index, room_slot.walk_in, room_slot.doctor_id, room_slot.patient_id))
        else:
            cur.execute("UPDATE ROOM_SLOTS SET (room_id=%s, slot_id=%s, walk_in=%s, doctor_id=%s, patient_id=%s) WHERE id=%s", (room_slot.room_id, room_slot.slot_yearly_index, room_slot.walk_in, room_slot.doctor_id, room_slot.patient_id, room_slot.id))
        connection.commit()
        cur.close()

    def delete_room_slot(self, room_slot_id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("DELETE FROM ROOM_SLOTS WHERE id=%s", [room_slot_id])
        connection.commit()
        cur.close()

    def update_patient(self, id, first_name, last_name, health_card, birthday, gender, phone_number, physical_address, email):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("UPDATE PATIENTS LEFT JOIN USERS ON PATIENTS.user_fk = USERS.id SET first_name = %s, last_name = %s, health_card = %s, birthday = %s, gender = %s, phone_number = %s, physical_address = %s, email = %s WHERE PATIENTS.id = %s", (first_name, last_name, health_card, birthday, gender, phone_number, physical_address, email, id))
        cur.close()
