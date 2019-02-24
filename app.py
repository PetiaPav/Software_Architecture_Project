from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from model.Tdg import Tdg
from model.Forms import PatientForm, DoctorForm, NurseForm, AppointmentForm
from passlib.hash import sha256_crypt
from functools import wraps


app = Flask(__name__)
tdg = Tdg(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET'])
def register():
    form = PatientForm(request.form)
    return render_template('register.html', form=form)


@app.route('/register/patient', methods=['POST'])
def register_patient():
    form = get_registration_form("patient", request.form)
    if request.method == 'POST' and form.validate():
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


@app.route('/register/doctor', methods=['POST'])
def register_doctor():
    form = get_registration_form("doctor", request.form)
    if request.method == 'POST' and form.validate():
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


@app.route('/register/nurse', methods=['POST'])
def register_nurse():
    form = get_registration_form("nurse", request.form)
    if request.method == 'POST' and form.validate():
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


def get_registration_form(user_type, form):
    if user_type == "patient":
        return PatientForm(form)
    elif user_type == 'doctor':
        return DoctorForm(form)
    elif user_type == 'nurse':
        return NurseForm(form)
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    # TODO as above.
    if request.method == 'POST':
        form = PatientForm(request.form)
        email = form.email.data
        password_candidate = form.password.data
        user = tdg.get_patient_by_email(email)
        if user:
            if sha256_crypt.verify(password_candidate, user['password']):
                session['logged_in'] = True
                session['email'] = user['email']
                session['first_name'] = user['first_name']
                session['id'] = user['id']
                session['type'] = 'patient'
                flash('You are now logged in', 'success')
                return redirect(url_for('patient_dashboard'))
            else:
                flash('Wrong password', 'danger')
        else:
            flash('Incorrect username', 'danger')
    return render_template('login.html')


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


@app.route('/patient_dashboard')
@is_logged_in
def patient_dashboard():
    return render_template('patient_dashboard.html')


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


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
