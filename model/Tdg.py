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
        return cur.lastrowid

    def insert_doctor(self, first_name, last_name, password, permit_number, specialty, city):
        connection = self.mysql.connect()
        cur = connection.cursor()

        cur.execute("INSERT INTO USERS(id, first_name, last_name, password) VALUES (NULL, %s, %s, %s)",
                    (first_name, last_name, password))
        last_inserted_id = cur.lastrowid

        cur.execute("INSERT INTO DOCTORS(id, user_fk, permit_number, specialty, city) VALUES(NULL, %s, %s, %s, %s)",
                    (last_inserted_id, permit_number, specialty, city))
        last_inserted_doctor_id = cur.lastrowid

        cur.close()
        connection.commit()
        return last_inserted_doctor_id

    def insert_nurse(self, first_name, last_name, password, access_id):
        connection = self.mysql.connect()
        cur = connection.cursor()

        cur.execute("INSERT INTO USERS(id, first_name, last_name, password) VALUES (NULL, %s, %s, %s)",
                    (first_name, last_name, password))
        last_inserted_id = cur.lastrowid

        cur.execute("INSERT INTO NURSES(id, user_fk, access_id) VALUES(NULL, %s, %s)", (last_inserted_id, access_id))

        last_inserted_nurse_id = cur.lastrowid
        cur.close()
        connection.commit()
        return last_inserted_nurse_id

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

    def get_all_clinics(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM UBER_CLINICS")
        clinics = []
        for clinic in cur:
            clinics.append(clinic)
        cur.close()
        return clinics
    
    def get_clinic_by_id(self, id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM UBER_CLINICS WHERE id =%s", [id])
        clinic_data = cur.fetchone()
        cur.close()
        if result is None:
            return False
        else:
            return clinic_data
            
    def insert_clinic(self, physical_address, name, start_time, end_time):
        connection = self.mysql.connect()
        cur = connection.cursor()

        cur.execute("INSERT INTO UBER_CLINICS (id, physical_address, name, start_time, end_time) VALUES (NULL, %s, %s, %s, %s)",
                    (physical_address, name, start_time, end_time))

        cur.close()
        connection.commit()

    def update_clinic(self, id, physical_address, name, start_time, end_time):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("UPDATE UBER_CLINICS SET physical_address = %s, name = %s, start_time = %s, end_time = %s WHERE UBER_CLINICS.id = %s", (physical_address, name, start_time, end_time, id))
        cur.close()

    def get_all_rooms(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM ROOMS LEFT JOIN UBER_CLINICS CLINIC ON (ROOMS.clinic_id = CLINIC.id WHERE id =%s", [id])
        rooms = []
        for room in cur:
            rooms.append(room)
        cur.close()
        return rooms

    def get_room_by_id(self, id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM ROOMS LEFT JOIN UBER_CLINICS CLINIC ON (ROOMS.clinic_id = CLINIC.id WHERE id =%s", [id])
        room_data = cur.fetchone()
        cur.close()
        if result is None:
            return False
        else:
            return room_data
    
    def update_room(self, id, name, clinic_id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("UPDATE ROOMS LEFT JOIN UBER_CLINICS ON ROOMS.clinic_id = UBER_CLINICS.id SET name = %s WHERE ROOMS.id = %s", (name, id))
        cur.close()

    def get_all_doctor_clinic_assignments(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM DOCTOR_CLINIC_ASSIGNMENT")
        clinic_doctor_assignments = []
        for clinic_doctor_assignment in cur:
            clinic_doctor_assignments.append(clinic_doctor_assignment)
        cur.close()
        return clinic_doctor_assignments

    def get_rooms_by_clinic_id(self, clinic_id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM ROOMS WHERE clinic_id=%s", [clinic_id])
        rooms = []
        for room in cur:
            room.append(room)
        cur.close()
        if len(rooms) > 0:
            return rooms
        else:
            return None

    def update_patient(self, id, first_name, last_name, health_card, birthday, gender, phone_number, physical_address, email):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("UPDATE PATIENTS LEFT JOIN USERS ON PATIENTS.user_fk = USERS.id SET first_name = %s, last_name = %s, health_card = %s, birthday = %s, gender = %s, phone_number = %s, physical_address = %s, email = %s WHERE PATIENTS.id = %s", (first_name, last_name, health_card, birthday, gender, phone_number, physical_address, email, id))
        cur.close()

    def insert_appointment(self, clinic_id, room_id, doctor_id, patient_id, date_time, walk_in):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute( "INSERT INTO APPOINTMENTS (id, clinic_id, room_id, doctor_id, patient_id, date_time, walk_in) VALUES (NULL, %s, %s, %s, %s, %s, %s)",(clinic_id, room_id, doctor_id, patient_id, convert_to_sql_datetime(date_time), walk_in))
        last_inserted_id = cur.lastrowid
        cur.close()
        return last_inserted_id

    def get_all_appointments(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute( "SELECT * FROM APPOINTMENTS")
        appointments = []
        for appt in cur:
            appointments.append(appt)
        cur.close()
        return appointments

    def remove_appointment(self, id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("DELETE FROM APPOINTMENTS WHERE id = %s", id)
        cur.close()
