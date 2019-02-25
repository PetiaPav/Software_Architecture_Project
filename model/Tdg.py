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
        cur.execute("SELECT * FROM PATIENTS WHERE email = %s", [email])
        data = cur.fetchone()
        cur.close()
        if data is None:
            return False
        else:
            return data


