from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, jsonify

from model import Forms
from model.Tdg import Tdg
from model.Forms import PatientForm, DoctorForm, NurseForm
from passlib.hash import sha256_crypt
from functools import wraps
from model.LoginAuthenticator import LoginDoctorAuthenticator, LoginNurseAuthenticator, LoginPatientAuthenticator
from model.ClinicRegistry import ClinicRegistry
from model.UserRegistry import UserRegistry
from model.AppointmentRegistry import AppointmentRegistry
from model.Scheduler import Scheduler
from model.Tool import Tools
from datetime import datetime
from model.Payment import Payment


def create_app(db_env="ubersante", debug=False):
    print("Loading app . . . ")
    app = Flask(__name__)
    tdg = Tdg(app, db_env)
    app.secret_key = 'secret123'
    app.debug = debug
    print("Loading User Registry . . . ")
    user_registry = UserRegistry.get_instance(tdg)
    print("Loading Clinic Registry . . . ")
    clinic_registry = ClinicRegistry.get_instance(tdg, user_registry.doctor.get_all())
    print("Loading Appointment Registry . . . ")
    appointment_registry = AppointmentRegistry.get_instance(tdg, clinic_registry, user_registry)


    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/register/patient', methods=['GET', 'POST'])
    def register_patient():
        form = get_registration_form("patient", request.form)

        if request.method == 'GET':
            return render_template('includes/_patient_form.html', form=form)

        elif request.method == 'POST' and form.validate():
            if user_registry.patient.get_by_email(form.email.data) is not None:
                flash ('This e-mail address has already been registered.', 'danger')
                return render_template('includes/_patient_form.html', form=form)
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

            inserted_id = tdg.insert_patient(email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address)
            user_registry.patient.insert_patient(inserted_id, email, password, first_name, last_name, health_card, phone_number,
                                                 birthday, gender, physical_address)
            flash('You are now registered and can log in!', 'success')
            return redirect(url_for('login'))

        return render_template('includes/_patient_form.html', form=form)

    @app.route('/register/doctor', methods=['GET', 'POST'])
    def register_doctor():
        form = get_registration_form("doctor", request.form)

        if request.method == 'GET':
            return render_template('includes/_doctor_form.html', form=form)

        elif request.method == 'POST' and form.validate():
            if user_registry.doctor.get_by_permit_number(form.permit_number.data) is not None:
                flash ('This permit number has already been registered.', 'danger')
                return render_template('includes/_doctor_form.html', form=form)
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

        return render_template('includes/_doctor_form.html', form=form)

    @app.route('/register/nurse', methods=['GET', 'POST'])
    def register_nurse():
        form = get_registration_form("nurse", request.form)

        if request.method == 'GET':
            return render_template('includes/_nurse_form.html', form=form)

        elif request.method == 'POST' and form.validate():
            if user_registry.nurse.get_by_access_id(form.access_id.data) is not None:
                flash ('This Access ID has already been registered.', 'danger')
                return render_template('includes/_nurse_form.html', form=form)
            # Common user attributes
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = sha256_crypt.hash(str(form.password.data))

            # Nurse attributes
            access_id = form.access_id.data

            tdg.insert_nurse(first_name, last_name, password, access_id)
            flash('You are now registered and can log in!', 'success')
            return redirect(url_for('login'))

        return render_template('includes/_nurse_form.html', form=form)

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
        session['selected_patient'] = id
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

        if not session['has_selected_walk_in']:
            type = "annual"
        else:
            type = "walk-in"
        return render_template('calendar.html', clinic = clinic, type_of_appointment = type)

    @app.route('/calendar_doctor')
    @is_logged_in
    def calendar_doctor():
        return render_template('calendar_doctor.html')

    @app.route('/doctor_view_schedule')
    @is_logged_in
    def doctor_view_schedule():
        return render_template('calendar_doctor_schedule_view.html')

    @app.route('/create_schedule')
    @is_logged_in
    def doctor_create_schedule():
        return render_template('calendar_doctor.html')

    @app.route('/view_patient_appointments')
    @is_logged_in
    def view_patient_appointments():
        appointment_info = view_appointments_for_user(session["id"])

        return render_template('includes/_view_patient_appointments.html', appointment_info=appointment_info)

    @app.route('/view_patient_appointments/<id>')
    @is_logged_in
    @nurse_login_required
    def view_selected_patient_appointments(id):

        session['selected_patient'] = int(id)
        appointment_info = view_appointments_for_user(int(id))
        return render_template('includes/_view_patient_appointments.html', appointment_info=appointment_info)

    def view_appointments_for_user(id):
        selected_patient = user_registry.patient.get_by_id(id)
        appointments_ids = selected_patient.appointment_ids
        patient_appointments = []
        appointment_clinics = []
        date_list = []
        time_list = []
        for id in appointments_ids:
            appointment = appointment_registry.get_appointment_by_id(id)
            patient_appointments.append(appointment)
            appointment_clinics.append(clinic_registry.get_by_id(appointment.clinic_id))
            appointment_date_time = Tools.get_date_time_from_slot_yearly_index(int(appointment.appointment_slot.slot_yearly_index))

            appointment_datetime = datetime.strptime(appointment_date_time, '%Y-%m-%dT%H:%M:%S')
            appointment_date = appointment_datetime.date().isoformat()
            appointment_time = appointment_datetime.time().isoformat()

            date_list.append(appointment_date)
            time_list.append(appointment_time)

        return zip(patient_appointments, appointment_clinics, date_list, time_list)

    @app.route('/delete_appointments/<appointment_id>/<patient_id>/<doctor_id>')
    @is_logged_in
    def delete_appointments(appointment_id, patient_id, doctor_id):
        # Delete the appointment for good
        appointment_registry.delete_appointment(int(appointment_id))
        user_registry.patient.delete_appointment(int(patient_id), int(appointment_id))
        user_registry.doctor.delete_appointment(int(doctor_id), int(appointment_id))
        return redirect(url_for('view_patient_appointments'))

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

        user_type = session['user_type']
        selected_patient = user_registry.patient.get_by_id(13)
        return render_template('appointment.html', eventid=id, clinic=clinic, walk_in=session['has_selected_walk_in'], date=selected_date, time=selected_time, datetime=str(selected_datetime), user_type = user_type, selected_patient = selected_patient)

    @app.route('/book_for_patient', methods=["POST"])
    @is_logged_in
    def book_for_patient():
        clinic = clinic_registry.get_by_id(request.json['clinic_id'])
        start_time = request.json['start']
        is_walk_in = (request.json['walk_in'] == 'True')

        new_appointment_id = appointment_registry.add_appointment(session['selected_patient'], clinic, start_time, is_walk_in)
        user_registry.patient.insert_appointment_ids(int(session['selected_patient']), [new_appointment_id])
        doctor_id = appointment_registry.get_appointment_by_id(new_appointment_id).appointment_slot.doctor_id
        user_registry.doctor.add_appointment_id(int(doctor_id), new_appointment_id)

        result = {
            'url': url_for('view_patient_appointments', id = str(session['selected_patient']))
        }
        return jsonify(result)

    @app.route('/cart', methods=["GET", "POST"])
    @is_logged_in
    def cart():
        if request.method == 'GET':  # view cart
            cart = user_registry.patient.get_by_id(session['id']).cart
            return render_template('cart.html', items=cart.item_dict)
        elif request.method == 'POST':  # add item to cart
            clinic = clinic_registry.get_by_id(request.json['clinic_id'])
            start_time = request.json['start']
            is_walk_in = (request.json['walk_in'] == 'True')

            cart = user_registry.patient.get_by_id(session['id']).cart
            add_item_status = cart.add(clinic, start_time, is_walk_in)
            result = {
                'url': url_for('cart'),
                'status': str(add_item_status)
            }
            return jsonify(result)

    @app.route('/cart/remove/<id>', methods=["POST"])
    @is_logged_in
    def remove_from_cart(id):  # remove item from cart
        id = int(id)
        cart = user_registry.patient.get_by_id(session['id']).cart
        cart.remove(id)
        result = {'url': url_for('cart')}
        return jsonify(result)

    @app.route('/checkout', methods={"POST"})
    @is_logged_in
    def checkout():  # checkout cart
        patient = user_registry.patient.get_by_id(session['id'])  # Get patient from user registry
        checkout_result = appointment_registry.checkout_cart(patient.cart.get_all(), patient.id)  # Save checkout result

        appointment_ids = checkout_result['accepted_appt_ids']
        user_registry.patient.insert_appointment_ids(patient.id, appointment_ids)

        appointments_created = []
        for appt_id in appointment_ids:
            appointments_created.append(appointment_registry.get_appointment_by_id(appt_id))

        user_registry.doctor.update_appointment_ids(appointments_created)

        patient.cart.batch_remove(checkout_result['accepted_items'])  # Removing successfully added items from cart
        patient.cart.batch_mark_booked(checkout_result['rejected_items'])  # Mark unavailable items in cart for frontend

        # Until appointments are paid, will remain in session
        if 'items_to_pay' in session:
            session['items_to_pay'] += checkout_result['accepted_items_is_walk_in']
        else:
            session['items_to_pay'] = checkout_result['accepted_items_is_walk_in']

        url = url_for('payment')
        if len(checkout_result['rejected_items']) != 0:
            url = url_for('cart')
        result = {'url': url}

        return jsonify(result)

    @app.route('/payment', methods=["GET", "POST"])
    @is_logged_in
    def payment():
        user_type = session['user_type']
        step = "payment"
        payment = None
        date = datetime.today().strftime('%Y-%m-%d')
        user = user_registry.patient.get_by_id(session['id'])
        # TODO: Replace with clinic id that was used for payment
        clinic = session['selected_clinic']
        if request.method == "POST":
            payment = Payment(session['items_to_pay'])
            session.pop('items_to_pay')
            payment.initialize()
            step = "receipt"
        return render_template('payment.html', user_type=user_type, date=date, step=step, user=user, clinic=clinic, payment=payment)

    @app.route('/doctor_schedule', methods=["GET", "POST"])
    @is_logged_in
    def return_doctor_schedule():
        if request.method == 'GET':
            return user_registry.doctor.get_schedule_by_week(session['id'], request.args['start'], appointment_registry.get_appointments_by_doctor_id_and_week(session['id'], Tools.get_week_index_from_date(request.args['start'])))

        if request.method == 'POST':
            user_registry.doctor.set_availability_from_json(session['id'], request.json)
            result = {'url': url_for('doctor_view_schedule')}
            return jsonify(result)

    @app.route('/doctor_update_schedule', methods=["POST"])
    @is_logged_in
    def updated_doctor_schedule():

        user_registry.doctor.set_special_availability_from_json(session['id'], request.json)
        result = {'url': url_for('doctor_view_schedule')}
        return jsonify(result)

    return app


if __name__ == "__main__":
    app = create_app(db_env="ubersante", debug=True)
    app.run()
