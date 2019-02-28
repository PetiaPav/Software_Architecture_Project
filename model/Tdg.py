from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


class Tdg:
    def __init__(self, app):
        self.mysql = MySQL(cursorclass=DictCursor)

        # Config MySQL
        app.config['MYSQL_DATABASE_USER'] = 'soen344'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'ubersante'
        app.config['MYSQL_DATABASE_DB'] = 'ubersante'
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

    def insert_appointment(self, patient_id, doctor_id, clinic_id, room, start_time, end_time):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO APPOINTMENTS(id, patient_id, doctor_id, clinic_id, room, start_time, end_time) VALUES(NULL, %s, %s, %s, %s, %s, %s)""",
                    (patient_id, doctor_id, clinic_id, room, start_time, end_time))
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

    def get_all_patients(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM PATIENTS")
        patients = []
        for row in cur.fetchall():
            patients.append(row)
        if patients is None:
            return False
        cur.close()
        return patients

    def get_all_nurses(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM NURSES")
        nurses = []
        for row in cur.fetchall():
            nurses.append(row)
        if nurses is None:
            return False
        cur.close()
        return nurses

    def get_all_doctors(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("SELECT * FROM DOCTORS")
        doctors = []
        for row in cur.fetchall():
            doctors.append(row)
        if doctors is None:
            return False
        cur.close()
        return doctors

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

    def get_patient_by_id(self, id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM PATIENTS WHERE id =%s", [id])
        patient_data = cur.fetchone()
        cur.close()
        if result is None:
            return False
        else:
            return patient_data

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



