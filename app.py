from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, jsonify

from model import Forms
from model.Forms import PatientForm, DoctorForm, NurseForm, ClinicForm
from passlib.hash import sha256_crypt
from functools import wraps
from model.LoginAuthenticator import LoginDoctorAuthenticator, LoginNurseAuthenticator, LoginPatientAuthenticator
from model.Tools import Tools
from datetime import datetime
from model.Payment import Payment
from model.Mediator import Mediator


def create_app(db_env="ubersante", debug=False):
    print("Loading app . . . ")
    app = Flask(__name__)
    app.secret_key = 'secret123'
    app.debug = debug
    mediator = Mediator.get_instance(app, db_env)

    @app.before_request
    def before_request():
        if session and 'user_type' in session:
            user = None
            if session['user_type'] == 'patient':
                user = mediator.get_patient_by_id(session['id'])
            elif session['user_type'] == 'doctor':
                user = mediator.get_doctor_by_id(session['id'])

            if user.has_new_appointment_notification:
                flash('New appointment(s) scheduled!', 'dark')
                user.has_new_appointment_notification = False

            if user.has_deleted_appointment_notification:
                flash('An appointment was canceled!', 'dark')
                user.has_deleted_appointment_notification = False

            if user.has_updated_appointment_notification:
                flash('An appointment was updated!', 'dark')
                user.has_updated_appointment_notification = False

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/register')
    def register():
        return render_template('register_choice.html')

    @app.route('/register/patient', methods=['GET', 'POST'])
    def register_patient():
        form = get_registration_form("patient", request.form)

        if request.method == 'GET':
            return render_template('includes/_patient_form.html', form=form)

        elif request.method == 'POST' and form.validate():
            if mediator.get_patient_by_email(form.email.data) is not None:
                flash('This e-mail address has already been registered.', 'danger')
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

            mediator.register_patient(email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address)
            flash('You are now registered and can log in!', 'success')
            return redirect(url_for('login'))

        return render_template('includes/_patient_form.html', form=form)

    @app.route('/register/doctor', methods=['GET', 'POST'])
    def register_doctor():
        form = get_registration_form("doctor", request.form)

        if request.method == 'GET':
            return render_template('includes/_doctor_form.html', form=form)

        elif request.method == 'POST' and form.validate():
            if mediator.get_doctor_by_permit_number(form.permit_number.data) is not None:
                flash('This permit number has already been registered.', 'danger')
                return render_template('includes/_doctor_form.html', form=form)
            # Common user attributes
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = sha256_crypt.hash(str(form.password.data))

            # Doctor attributes
            permit_number = form.permit_number.data
            specialty = form.specialty.data
            city = form.city.data

            mediator.register_doctor(first_name, last_name, password, permit_number, specialty, city)
            flash('You are now registered and can log in!', 'success')
            return redirect(url_for('login'))

        return render_template('includes/_doctor_form.html', form=form)

    @app.route('/register/nurse', methods=['GET', 'POST'])
    def register_nurse():
        form = get_registration_form("nurse", request.form)

        if request.method == 'GET':
            return render_template('includes/_nurse_form.html', form=form)

        elif request.method == 'POST' and form.validate():
            if mediator.get_nurse_by_access_id(form.access_id.data) is not None:
                flash('This Access ID has already been registered.', 'danger')
                return render_template('includes/_nurse_form.html', form=form)
            # Common user attributes
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = sha256_crypt.hash(str(form.password.data))

            # Nurse attributes
            access_id = form.access_id.data

            mediator.register_nurse(first_name, last_name, password, access_id)
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
                if form.authenticate_user(mediator.get_user_by_unique_login_identifier(form.unique_identifier, form.unique_identifier_value.data)):
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
        elif user_type == 'clinic':
            return ClinicForm(form)
        return None

    def is_logged_in(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash('Unauthorized, please log in', 'danger')
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

        nb_upcoming_appointments = 0
        if user_type == 'patient':
            patient = mediator.get_patient_by_id(session['id'])
            nb_upcoming_appointments = len(patient.appointment_dict)
        if user_type == 'doctor':
            doctor = mediator.get_doctor_by_id(session['id'])
            nb_upcoming_appointments = len(doctor.appointment_dict)

        return render_template('dashboard.html', user_type=user_type, nb_upcoming_appointments=nb_upcoming_appointments)

    @app.route('/dashboard/patient_info')
    @is_logged_in
    def patient_info():
        selected_patient = mediator.get_patient_by_id(session["id"])
        return render_template('includes/_patient_detail_page.html', patient=selected_patient)

    @app.route('/dashboard/patient_registry')
    @is_logged_in
    @nurse_login_required
    def patient_registry():
        all_patients = mediator.get_all_patients()
        return render_template('includes/_patient_registry.html', all_patients=all_patients)

    @app.route('/dashboard/nurse_info')
    @is_logged_in
    def nurse_info():
        selected_nurse = mediator.get_nurse_by_id(session["id"])
        return render_template('includes/_nurse_detail_page.html', nurse=selected_nurse)

    @app.route('/dashboard/nurse_registry')
    @is_logged_in
    @nurse_login_required
    def nurse_registry():
        all_nurses = mediator.get_all_nurses()
        return render_template('includes/_nurse_registry.html', all_nurses=all_nurses)

    @app.route('/dashboard/doctor_registry')
    @is_logged_in
    @nurse_login_required
    def doctor_registry():
        all_doctors = mediator.get_all_doctors()
        return render_template('includes/_doctor_registry.html', all_doctors=all_doctors)

    @app.route('/dashboard/patient_registry/<id>', methods=['GET'])
    @is_logged_in
    @nurse_login_required
    def patient_detailed_page(id):
        session['selected_patient'] = id
        patient = mediator.get_patient_by_id(id)
        return render_template('includes/_patient_detail_page.html', patient=patient)

    @app.route('/calendar')
    @is_logged_in
    def make_appointment_calendar():
        clinic = mediator.get_clinic_by_id(session['selected_clinic'])

        if not session['has_selected_walk_in']:
            type = "annual"
        else:
            type = "walk-in"
        return render_template('calendar.html', clinic=clinic, type_of_appointment=type)

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
        appointment_info = view_appointments_for_user(session["id"], 'patient')
        return render_template('includes/_view_patient_appointments.html', patient_id=session["id"], appointment_info=appointment_info)

    @app.route('/view_doctor_appointments')
    @is_logged_in
    def view_doctor_appointments():
        appointment_info = view_appointments_for_user(session["id"], 'doctor')
        return render_template('includes/_view_doctor_appointments.html', doctor_id=session["id"],
                               appointment_info=appointment_info)

    @app.route('/view_selected_patient_appointments/<id>')
    @is_logged_in
    def view_selected_patient_appointments(id):
        session['selected_patient'] = int(id)
        appointment_info = view_appointments_for_user(int(id), 'patient')
        return render_template('includes/_view_patient_appointments.html', patient_id=id, appointment_info=appointment_info)

    def view_appointments_for_user(user_id, user_type):
        selected_user = None
        user_appointments = None
        if user_type == 'patient':
            selected_user = mediator.get_patient_by_id(user_id)
            user_appointments = selected_user.appointment_dict.values()
        elif user_type == 'doctor':
            selected_user = mediator.get_doctor_by_id(user_id)
            user_appointments = selected_user.appointment_dict.values()

        appointment_clinics = []
        date_list = []
        time_list = []
        for appointment in user_appointments:
            appointment_clinics.append(appointment.clinic)

            appointment_date = appointment.date_time.date().isoformat()
            appointment_time = appointment.date_time.time().isoformat()

            date_list.append(appointment_date)
            time_list.append(appointment_time)

        return zip(user_appointments, appointment_clinics, date_list, time_list)


    @app.route('/modify_appointments/<patient_id>/<appointment_id>')
    @is_logged_in
    def modify_appointments(patient_id, appointment_id):
        session['selected_appointment'] = appointment_id
        # return redirect(url_for('select_clinic'))
        return render_template('includes/_select_clinic.html', clinics=mediator.get_all_clinics())

    @app.route('/delete_appointments/<patient_id>/<appointment_id>')
    @is_logged_in
    def delete_appointments(patient_id, appointment_id):
        mediator.delete_appointment(int(appointment_id))
        return redirect(url_for('view_selected_patient_appointments', id=patient_id))

    @app.route('/select_clinic')
    @is_logged_in
    def add_appointment():
        return render_template('includes/_select_clinic.html', clinics=mediator.get_all_clinics())

    @app.route('/select_clinic/<id>')
    @is_logged_in
    def select_appointment_type(id):
        session['selected_clinic'] = id
        return render_template('includes/_appointment_type.html', clinics=mediator.get_all_clinics())

    @app.route('/view_calendar/<type>')
    @is_logged_in
    def view_calendar(type):
        session['has_selected_walk_in'] = (type != "annual")
        return redirect(url_for('make_appointment_calendar'))

    @app.route('/return_weekly_availabilities', methods=["GET", "POST"])
    @is_logged_in
    def return_weekly_availabilities():
        date_time = Tools.convert_to_python_datetime(str(request.args.get('start')))
        result = mediator.find_availability(int(session['selected_clinic']), date_time, session['has_selected_walk_in']) 
        return result if result is not None else Tools.get_unavailable_times_message(date_time)

    @app.route('/show_event_details', methods=["POST"])
    @is_logged_in
    def show_event_details():
        event_id = request.json['id']
        if event_id == 'expired':
            return url_for('make_appointment_calendar')

        if session['selected_appointment'] is not None:
            return url_for('update_selected_appointment', event_id=event_id, start=request.json['start'])
        else:
            return url_for('selected_appointment', event_id=event_id, start=request.json['start'])

    @app.route('/selected_appointment/<start>')
    @is_logged_in
    def selected_appointment(start):
        clinic = mediator.get_clinic_by_id(session['selected_clinic'])
        if not session['has_selected_walk_in']:
            appointment_type = "Annual"
        else:
            appointment_type = "Walk-in"

        selected_datetime = Tools.convert_to_python_datetime(start)
        selected_date = Tools.get_date_iso_format(selected_datetime)
        selected_time = Tools.get_time_iso_format(selected_datetime)

        user_type = session['user_type']
        
        patient_id = session['selected_patient'] if user_type == 'nurse' else session['id']

        selected_patient = mediator.get_patient_by_id(patient_id)
        return render_template('appointment.html', clinic=clinic, walk_in=session['has_selected_walk_in'], date=selected_date, time=selected_time, datetime=str(selected_datetime), user_type=user_type, selected_patient=selected_patient)

    @app.route('/view_scheduled_appointment_details/<appointment_id>', methods=['GET'])
    def view_scheduled_appointment_details(appointment_id):
        selected_appointment = mediator.get_appointment_by_id(appointment_id)

        clinic = selected_appointment.clinic
        walk_in = selected_appointment.walk_in
        date = Tools.get_date_iso_format(selected_appointment.date_time)
        time = Tools.get_time_iso_format(selected_appointment.date_time)
        datetime = str(selected_appointment.date_time)
        user_type = session['user_type']
        selected_patient = selected_appointment.patient

        return render_template('appointment.html', clinic=clinic, walk_in=walk_in,
                               date=date, time=time, datetime=datetime,
                               user_type=user_type, selected_patient=selected_patient)

    @app.route('/update_selected_appointment/<event_id>/<start>')
    @is_logged_in
    def update_selected_appointment(event_id, start):
        appointment_to_modify = mediator.get_appointment_by_id(session['selected_appointment'])
        session['selected_appointment'] = None
        clinic = mediator.get_clinic_by_id(session['selected_clinic'])
        if not session['has_selected_walk_in']:
            appointment_type = "Annual"
        else:
            appointment_type = "Walk-in"

        selected_datetime = Tools.convert_to_python_datetime(start)
        selected_date = Tools.get_date_iso_format(selected_datetime)
        selected_time = Tools.get_time_iso_format(selected_datetime)

        appointment_to_modify_date = Tools.get_date_iso_format(appointment_to_modify.date_time)
        appointment_to_modify_time = Tools.get_time_iso_format(appointment_to_modify.date_time)

        user_type = session['user_type']

        patient_id = session['selected_patient'] if user_type == 'nurse' else session['id']

        selected_patient = mediator.get_patient_by_id(patient_id)
        return render_template('update_appointment.html', clinic=clinic,
                               walk_in=session['has_selected_walk_in'], date=selected_date, time=selected_time,
                               datetime=str(selected_datetime), user_type=user_type, selected_patient=selected_patient,
                               appointment_to_modify = appointment_to_modify, appointment_to_modify_date = appointment_to_modify_date,
                               appointment_to_modify_time = appointment_to_modify_time)

    @app.route('/book_for_patient', methods=["POST"])
    @is_logged_in
    def book_for_patient():
        is_walk_in = (request.json['walk_in'] == 'True')
        selected_date_time = Tools.convert_to_python_datetime(request.json['start'])
        mediator.add_appointment(session['selected_patient'], request.json['clinic_id'], selected_date_time, is_walk_in)

        result = {
            'url': url_for('view_selected_patient_appointments', id=str(session['selected_patient']))
        }
        return jsonify(result)

    @app.route('/modify_appointment', methods=["POST"])
    @is_logged_in
    def modify_appointment():
        is_walk_in = (request.json['walk_in'] == 'True')
        selected_date_time = Tools.convert_to_python_datetime(request.json['start'])
        mediator.update_appointment(request.json['old_appointment_id'], request.json['clinic_id'], selected_date_time, is_walk_in)

        result = None

        if session['user_type'] == 'nurse':
            result = {
                'url': url_for('view_selected_patient_appointments', id=str(session['selected_patient']))
            }
        elif session['user_type'] == 'patient':
            result = {
                'url': url_for('view_selected_patient_appointments', id=str(session['id']))
            }
        return jsonify(result)

    @app.route('/cart', methods=["GET", "POST"])
    @is_logged_in
    def cart():
        if request.method == 'GET':  # view cart
            cart = mediator.get_patient_cart(session['id'])
            return render_template('cart.html', items=cart.item_dict)
        elif request.method == 'POST':  # add item to cart
            clinic = mediator.get_clinic_by_id(request.json['clinic_id'])
            start_time = request.json['start']
            is_walk_in = (request.json['walk_in'] == 'True')

            selected_datetime = Tools.convert_to_python_datetime(start_time)

            cart = mediator.get_patient_cart(session['id'])
            add_item_status = cart.add(clinic, selected_datetime, is_walk_in)
            result = {
                'url': url_for('cart'),
                'status': str(add_item_status)
            }
            return jsonify(result)

    @app.route('/cart/remove/<id>', methods=["POST"])
    @is_logged_in
    def remove_from_cart(id):  # remove item from cart
        id = int(id)
        cart = mediator.get_patient_cart(session['id'])
        cart.remove(id)
        result = {'url': url_for('cart')}
        return jsonify(result)

    @app.route('/checkout', methods={"POST"})
    @is_logged_in
    def checkout_cart():
        # Get patient from user registry
        patient = mediator.get_patient_by_id(session['id'])

        # Save checkout result
        checkout_result = mediator.checkout_cart(patient.cart.get_all(), patient.id)

        # Removing successfully added items from cart
        patient.cart.batch_remove(checkout_result['accepted_items'])

        # Mark unavailable items in cart for frontend
        patient.cart.batch_mark_booked(checkout_result['rejected_items'])

        session['newly_booked_appointment_ids'] = checkout_result['accepted_appointments_ids']

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
        user = mediator.get_patient_by_id(session['id'])
        # TODO: Replace with clinic id that was used for payment
        clinic = session['selected_clinic']
        if request.method == "POST":
            payment = Payment(session['items_to_pay'])
            session.pop('items_to_pay')
            payment.initialize()
            step = "receipt"

            # This for loop needs to be inside the POST otherwise the user will be notified of new appointment before being done paying
            for appointment_id in session['newly_booked_appointment_ids']:
                appointment = mediator.get_appointment_by_id(appointment_id)
                appointment.notify("add")

            session['newly_booked_appointment_ids'] = []

        return render_template('payment.html', user_type=user_type, date=date, step=step, user=user, clinic=clinic, payment=payment)

    @app.route('/doctor_schedule', methods=["GET", "POST"])
    @is_logged_in
    def return_doctor_schedule():
        if request.method == 'GET':
            return mediator.get_doctor_schedule_by_week(int(session['id']), request.args['start'])
        if request.method == 'POST':
            mediator.set_doctor_generic_availability_from_json(session['id'], request.json)
            result = {'url': url_for('doctor_view_schedule')}
            return jsonify(result)

    @app.route('/doctor_update_schedule', methods=["POST"])
    @is_logged_in
    def updated_doctor_schedule():

        mediator.set_doctor_adjustments_from_json(session['id'], request.json)
        result = {'url': url_for('doctor_view_schedule')}
        return jsonify(result)

    @app.route('/insert_clinic', methods=["GET","POST"])
    @is_logged_in
    @nurse_login_required
    def insert_clinic():
        # Change dictionnary to tuple to work in frontend library
        doctors = mediator.get_all_doctors()
        doctors_tuple = []
        for doctor in doctors:
            doctors_tuple.append((doctor.id, doctor.first_name + " " + doctor.last_name))
        nurses = mediator.get_all_nurses()
        nurses_tuple = []
        for nurse in nurses:
            nurses_tuple.append((nurse.id, nurse.first_name + " " + nurse.last_name))
        form = get_registration_form("clinic", request.form)
        form.doctors.choices = doctors_tuple
        form.nurses.choices = nurses_tuple
        if request.method == 'GET':
            return render_template('clinic.html', form=form, update=False)
        if request.method == 'POST' and form.validate():
            mediator.register_clinic(form)
            flash('Clinic has been successfully inserted.', 'success')
            return redirect(url_for('dashboard'))
        return render_template('clinic.html', form=form, update=False)

    @app.route('/update_clinic', methods=["GET"])
    @is_logged_in
    @nurse_login_required
    def update_clinic():
        return render_template('includes/_select_clinic.html',clinics=mediator.get_all_clinics(), step="update")

    @app.route('/update_clinic/<id>', methods=["GET","POST"])
    @is_logged_in
    def update_clinic_selected(id):
        clinic_id = id
        # Change dictionnary to tuple to work in frontend library
        clinic = mediator.get_clinic_by_id(clinic_id)
        doctors = mediator.get_all_doctors()
        doctors_tuple = []
        for doctor in doctors:
            doctors_tuple.append((doctor.id, doctor.first_name + " " + doctor.last_name))
        nurses = mediator.get_all_nurses()
        nurses_tuple = []
        for nurse in nurses:
            nurses_tuple.append((nurse.id, nurse.first_name + " " + nurse.last_name))
        form = get_registration_form("clinic", request.form)
        form.doctors.choices = doctors_tuple
        form.nurses.choices = nurses_tuple
        if request.method == 'GET':
            form.name.data = clinic.name
            form.physical_address.data = clinic.physical_address
            form.start_time.data = clinic.business_hours.opening_time.strftime("%H:%M")
            form.end_time.data = clinic.business_hours.closing_time.strftime("%H:%M")
            form.rooms.data = len(clinic.rooms)
            return render_template('clinic.html', form=form, clinic=clinic, update=True)
        if request.method == 'POST' and form.validate():
            mediator.update_clinic(clinic, form)
            flash('Clinic has been successfully updated.', 'success')
            return redirect(url_for('dashboard'))
        return render_template('clinic.html', clinic=clinic, form=form, update=True)

    return app

if __name__ == "__main__":
    app = create_app(db_env="ubersante", debug=True)
    app.run()
