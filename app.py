from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from model.Tdg import Tdg
from model.Forms import PatientForm, DoctorForm, NurseForm, AppointmentForm
from passlib.hash import sha256_crypt
from functools import wraps
from model.LoginAuthenticator import LoginDoctorAuthenticator, LoginNurseAuthenticator, LoginPatientAuthenticator


def create_app(db_env="ubersante", debug=False):
    app = Flask(__name__)
    tdg = Tdg(app, db_env)
    app.secret_key = 'secret123'
    app.debug=debug

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/register/patient', methods=['GET','POST'])
    def register_patient():
        form = get_registration_form("patient", request.form)

        if request.method == 'GET':
            return render_template('includes/_patient_form.html', form=form)

        elif request.method == 'POST' and form.validate():
            # Common user attributes
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = sha256_crypt.hash(str(form.password.data))

            # Patient attributes
            email = form.email.data
            health_card = form.health_card.data
            phone_number = form.phone_number.data
            birthday = form.birthday.data
            gender = form.gender.data
            physical_address = form.physical_address.data

            tdg.insert_patient(email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address)
            flash('You are now registered and can log in!', 'success')
            return redirect(url_for('login'))

        flash('Server encountered error - Please try again later', 'error')
        return render_template('register.html', form=form)

    @app.route('/register/doctor', methods=['GET', 'POST'])
    def register_doctor():
        form = get_registration_form("doctor", request.form)

        if request.method == 'GET':
            return render_template('includes/_doctor_form.html', form=form)

        elif request.method == 'POST' and form.validate():
            # Common user attributes
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = sha256_crypt.hash(str(form.password.data))

            # Doctor attributes
            permit_number = form.permit_number.data
            specialty = form.specialty.data
            city = form.city.data

            tdg.insert_doctor(first_name, last_name, password, permit_number, specialty, city)
            flash('You are now registered and can log in!', 'success')
            return redirect(url_for('login'))

        flash('Server encountered error - Please try again later', 'error')
        return render_template('register.html', form=form)

    @app.route('/register/nurse', methods=['GET', 'POST'])
    def register_nurse():
        form = get_registration_form("nurse", request.form)

        if request.method == 'GET':
            return render_template('includes/_nurse_form.html', form=form)

        elif request.method == 'POST' and form.validate():
            # Common user attributes
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = sha256_crypt.hash(str(form.password.data))

            # Nurse attributes
            access_id = form.access_id.data

            tdg.insert_nurse(first_name, last_name, password, access_id)
            flash('You are now registered and can log in!', 'success')
            return redirect(url_for('login'))

        flash('Server encountered error - Please try again later', 'error')
        return render_template('register.html', form=form)

    @app.route('/login/<user_type>', methods=['GET', 'POST'])
    def login_user(user_type):
        form = None
        if user_type == 'patient':
            form = LoginPatientAuthenticator(request.form)
        elif user_type == 'doctor':
            form = LoginDoctorAuthenticator(request.form)
        elif user_type == 'nurse':
            form = LoginNurseAuthenticator(request.form)

        if request.method == 'POST':
            if form is not None and form.validate():
                if form.authenticate_user(tdg):
                    return redirect(url_for('dashboard'))

        return render_template('login.html', form=form, user_type=user_type)

    @app.route('/login')
    def login():
        return render_template('login_choice.html')

    def get_registration_form(user_type, form):
        if user_type == "patient":
            return PatientForm(form)
        elif user_type == 'doctor':
            return DoctorForm(form)
        elif user_type == 'nurse':
            return NurseForm(form)
        return None

    def is_logged_in(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash('Unauthroized, please log in', 'danger')
                return redirect(url_for('login'))
        return wrap

    @app.route('/logout')
    @is_logged_in
    def logout():
        session.clear()
        flash('You are now logged out!', 'success')
        return redirect(url_for('home'))

    @app.route('/dashboard')
    @is_logged_in
    def dashboard():
        user_type = session['user_type']
        return render_template('dashboard.html', user_type=user_type)

    @app.route('/add_appointment', methods=['GET', 'POST'])
    @is_logged_in
    def add_appointment():
        form = AppointmentForm(request.form)
        #TODO ids as fks
        if request.method == 'POST' and form.validate():
            patient_id = session['id']
            doctor_id = form.doctor_id.data
            clinic_id = 1
            room = form.room.data
            start_time = form.start_time.data
            end_time = form.end_time.data
            tdg.insert_appointment(patient_id, doctor_id, clinic_id, room, start_time, end_time)
            flash('Appointment created!', 'success')
            return redirect(url_for('patient_dashboard'))
        return render_template('add_appointment.html', form=form)

    @app.route('/calendar')
    @is_logged_in
    def calendar_example():
        return render_template('calendar.html')

    @app.route('/calendar_doctor')
    @is_logged_in
    def calendar_doctor():
        print("LOADING CALENDAR PAGE")
        return render_template('calendar_doctor.html')

    @app.route('/data', methods=["GET", "POST"])
    @is_logged_in
    def return_data():
        if request.method == 'GET':
            with open("test_events.json", "r") as input_data:
                return input_data.read()

        if request.method == 'POST':
            start_date = request.json['startDate']
            end_date = request.json['endDate']
            print(start_date)
            print(end_date)

            # Must return any real object
            return start_date

    @app.route('/event', methods=["POST"])
    @is_logged_in
    def show_event_details():
        return url_for('selected_appointment', id=request.json['id'])

    @app.route('/selected_appointment/<id>')
    @is_logged_in
    def selected_appointment(id):
        return render_template('appointment.html', eventid=id)

    return app

if __name__ == "__main__":
    app = create_app(db_env="ubersante", debug=True)
    app.run()