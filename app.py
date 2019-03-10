from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

from model import Forms
from model.Tdg import Tdg
from model.Forms import PatientForm, DoctorForm, NurseForm, AppointmentForm
from passlib.hash import sha256_crypt
from functools import wraps
from model.LoginAuthenticator import LoginDoctorAuthenticator, LoginNurseAuthenticator, LoginPatientAuthenticator
from model.ClinicRegistry import ClinicRegistry
from model.UserRegistry import UserRegistry
from model.AppointmentRegistry import AppointmentRegistry
from model.Scheduler import Scheduler
from datetime import datetime

def create_app(debug=False):
    print("Loading app . . . ")
    app = Flask(__name__)
    tdg = Tdg(app)
    print("Loading User Registry . . . ")
    user_registry = UserRegistry(tdg)
    print("Loading Clinic Registry . . . ")
    clinic_registry = ClinicRegistry(tdg, user_registry.doctor.get_all())
    print("Loading Appointment Registry . . . ")
    appointment_registry = AppointmentRegistry(clinic_registry)
    app.secret_key = 'secret123'
    app.debug = debug

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

    def nurse_login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if session['user_type'] != 'nurse':
                flash('Unauthorized, please log in as a nurse', 'danger')
                return redirect(url_for('login'))
            else:
                return f(*args, **kwargs)
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

    @app.route('/dashboard/patient_info')
    @is_logged_in
    def patient_info():
        selected_patient = user_registry.patient.get_by_id(session["id"])
        return render_template('includes/_patient_detail_page.html', patient=selected_patient)

    @app.route('/dashboard/patient_registry')
    @is_logged_in
    @nurse_login_required
    def patient_registry():
        all_patients = user_registry.patient.get_all()
        return render_template('includes/_patient_registry.html', all_patients=all_patients)

    @app.route('/dashboard/nurse_registry')
    @is_logged_in
    @nurse_login_required
    def nurse_registry():
        all_nurses = user_registry.nurse.get_all()
        return render_template('includes/_nurse_registry.html', all_nurses=all_nurses)

    @app.route('/dashboard/doctor_registry')
    @is_logged_in
    @nurse_login_required
    def doctor_registry():
        all_doctors = user_registry.doctor.get_all()
        return render_template('includes/_doctor_registry.html', all_doctors=all_doctors)

    @app.route('/dashboard/patient_registry/<id>', methods=['GET'])
    @is_logged_in
    @nurse_login_required
    def patient_detailed_page(id):
        get_patient = user_registry.patient.get_by_id(id)
        return render_template('includes/_patient_detail_page.html', patient = get_patient)

    @app.route('/edit/patient/<id>', methods=['GET', 'POST'])
    @is_logged_in
    @nurse_login_required
    def modify_patient(id):
        selected_patient = user_registry.patient.get_by_id(id)
        form = Forms.get_form_data("patient", selected_patient, request)

        if request.method == "POST" and form.validate():
            user_registry.patient.update_patient(id, request)
            return redirect(url_for('patient_registry'))
        else:
            return render_template('includes/_edit_patient_form.html', form=form, id=selected_patient.id)

    @app.route('/edit/doctor/<id>', methods=['GET', 'POST'])
    @is_logged_in
    @nurse_login_required
    def modify_doctor(id):
        selected_doctor = user_registry.doctor.get_by_id(id)
        form = Forms.get_form_data("doctor", selected_doctor, request)
        return render_template('includes/_edit_doctor_form.html', form=form)

    @app.route('/edit/nurse/<id>', methods=['GET', 'POST'])
    @is_logged_in
    @nurse_login_required
    def modify_nurse(id):
        selected_nurse = user_registry.nurse.get_by_id(id)
        form = Forms.get_form_data("nurse", selected_nurse, request)
        return render_template('includes/_edit_nurse_form.html', form=form)

    @app.route('/edit/personal_profile', methods=['GET', 'POST'])
    @is_logged_in
    @nurse_login_required
    def modify_personal_profile():
        selected_nurse = user_registry.nurse.get_by_access_id(session["access_id"])
        form = Forms.get_form_data("nurse", selected_nurse, request)
        return render_template('includes/_edit_nurse_form.html', form=form)

    @app.route('/calendar')
    @is_logged_in
    def make_appointment_calendar():
        clinic = clinic_registry.get_by_id(session['selected_clinic'])

        if session['has_selected_walk_in'] == False:
            type = "annual"
        else:
            type = "walk-in"
        return render_template('calendar.html', clinic = clinic, type_of_appointment = type)

    @app.route('/calendar_doctor')
    @is_logged_in
    def calendar_doctor():
        print("LOADING CALENDAR PAGE")
        return render_template('calendar_doctor.html')

    @app.route('/select_clinic')
    @is_logged_in
    def add_appointment():
        return render_template('includes/_select_clinic.html', clinics = clinic_registry.clinics)

    @app.route('/select_clinic/<id>')
    @is_logged_in
    def select_appointment_type(id):
        session['selected_clinic'] = id
        return render_template('includes/_appointment_type.html', clinics = clinic_registry.clinics)

    @app.route('/view_calendar/<type>')
    @is_logged_in
    def view_calendar(type):
        session['has_selected_walk_in'] = (type != "annual")
        return redirect(url_for('make_appointment_calendar'))

    @app.route('/data', methods=["GET", "POST"])
    @is_logged_in
    def return_weekly_availabilities():
        clinic = clinic_registry.get_by_id(session['selected_clinic'])
        return Scheduler.availability_finder(clinic, str(request.args.get('start')), session['has_selected_walk_in'])

    @app.route('/event', methods=["POST"])
    @is_logged_in
    def show_event_details():
        return url_for('selected_appointment', id=request.json['id'], start=request.json['start'])

    @app.route('/selected_appointment/<id>/<start>')
    @is_logged_in
    def selected_appointment(id, start):
        clinic = clinic_registry.get_by_id(session['selected_clinic'])
        if not session['has_selected_walk_in']:
            appointment_type = "Annual"
        else:
            appointment_type = "Walk-in"

        selected_datetime = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        selected_date = selected_datetime.date().isoformat()
        selected_time = selected_datetime.time().isoformat()
        return render_template('appointment.html', eventid=id, clinic=clinic, type=appointment_type, date=selected_date, time=selected_time)

    return app


if __name__ == "__main__":
    app = create_app(debug=True)
    app.run()
