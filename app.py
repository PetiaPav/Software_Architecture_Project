from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from model.Tdg import Tdg
from model.Forms import RegisterForm, AppointmentForm, LoginDoctorForm, LoginNurseForm, LoginPatientForm
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    # TODO either rename this and login, or create separate tabs on the respective pages.
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password=sha256_crypt.hash(str(form.password.data))
        first_name = form.first_name.data
        last_name = form.first_name.data
        health_card = form.health_card.data
        phone_number = form.phone_number.data
        birthday = form.birthday.data
        gender = form.gender.data
        physical_address = form.physical_address.data
        tdg.insert_patient(email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address)
        flash('You are now registered and can log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # TODO as above.
#     if request.method == 'POST':
#         form = RegisterForm(request.form)
#         email = form.email.data
#         password_candidate = form.password.data
#         user = tdg.get_patient_by_email(email)
#         if user:
#             if sha256_crypt.verify(password_candidate, user['password']):
#                 session['logged_in'] = True
#                 session['email'] = user['email']
#                 session['first_name'] = user['first_name']
#                 session['id'] = user['id']
#                 session['type'] = 'patient'
#                 flash('You are now logged in', 'success')
#                 return redirect(url_for('patient_dashboard'))
#             else:
#                 flash('Wrong password', 'danger')
#         else:
#             flash('Incorrect username', 'danger')
#     return render_template('login.html')

@app.route('/login/<user_type>', methods=['GET', 'POST'])
def login_user(user_type):
    form = None
    if user_type == 'patient':
        form = LoginPatientForm(request.form)
    elif user_type == 'doctor':
        form = LoginDoctorForm(request.form)
    elif user_type == 'nurse':
        form = LoginNurseForm(request.form)

    if request.method == 'POST':
        if form is not None and form.validate():
            if form.authenticate_user(tdg):
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form, user_type=user_type)


@app.route('/login')
def login():
    return render_template('login_choice.html')


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


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
