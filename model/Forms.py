from wtforms import Form, StringField, DateField, SelectField, TextAreaField, PasswordField, validators
from flask import session, flash
from passlib.hash import sha256_crypt


class RegisterForm(Form):
    email = StringField('Email')
    password = PasswordField('Password', [
        validators.EqualTo('confirm', message='Passwords do not match.')
    ])
    confirm = PasswordField('Confirm Password')
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    health_card = StringField('Health Card')
    phone_number = StringField('Phone Number')
    birthday = StringField('Birth Date')  # format='%d-%m-%Y'
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    physical_address = StringField('Address')


class LoginForm(Form):
    password = PasswordField('Password', [validators.Length(min=6)])


class LoginDoctorForm(LoginForm):
    physician_permit_number = StringField('Physician Permit Number', [validators.Length(min=7)])

    def authenticate_user(self, tdg):
        user = tdg.get_doctor_by_permit_number(self.physician_permit_number.data)
        if user:
            if sha256_crypt.verify(self.password.data, user["password"]):
                session['logged_in'] = True
                session['user_type'] = 'doctor'
                session['first_name'] = user['first_name']
                return True
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('No doctor registered with that physician permit number', 'danger')
        return False


class LoginNurseForm(LoginForm):
    access_id = StringField('Access ID', [validators.Length(min=8)])

    def authenticate_user(self, tdg):
        user = tdg.get_nurse_by_access_id(self.access_id.data)
        if user:
            if sha256_crypt.verify(self.password.data, user["password"]):
                session['logged_in'] = True
                session['user_type'] = 'nurse'
                session['first_name'] = user['first_name']
                return True
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('No nurse registered with that Access ID', 'danger')
        return False


class LoginPatientForm(LoginForm):
    email = StringField('Email', [validators.InputRequired(), validators.Length(min=5)])

    def authenticate_user(self, tdg):
        user = tdg.get_patient_by_email(self.email.data)
        if user:
            if sha256_crypt.verify(self.password.data, user["password"]):
                session['logged_in'] = True
                session['user_type'] = 'patient'
                session['first_name'] = user['first_name']
                return True
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('No user registered with that email address', 'danger')
        return False


class AppointmentForm(Form):
    doctor_id = SelectField('Doctor Name', choices=[('1', 'Ivanov'), ('2', 'Petrov')])
    room = SelectField('Room Number', choices=[('1', '1'), ('2', '2')])
    # TODO will need to properly validate and convert the times
    start_time = StringField('Start Time')
    end_time = StringField('Start Time')