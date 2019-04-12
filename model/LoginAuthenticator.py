from wtforms import Form, PasswordField, validators, StringField
from flask import session, flash
from passlib.hash import sha256_crypt


class LoginAuthenticator(Form):
    password = PasswordField('Password', [validators.Length(min=6)])


class LoginDoctorAuthenticator(LoginAuthenticator):
    unique_identifier_value = StringField('Physician Permit Number', [validators.Length(min=7)])
    unique_identifier = 'permit_number'

    def authenticate_user(self, user):
        if user:
            if sha256_crypt.verify(self.password.data, user.password):
                session['logged_in'] = True
                session['user_type'] = 'doctor'
                session['id'] = user.id
                session['first_name'] = user.first_name
                return True
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('No doctor registered with that physician permit number', 'danger')
        return False


class LoginNurseAuthenticator(LoginAuthenticator):
    unique_identifier_value = StringField('Access ID', [validators.Length(min=8)])
    unique_identifier = 'access_id'

    def authenticate_user(self, user):
        if user:
            if sha256_crypt.verify(self.password.data, user.password):
                session['logged_in'] = True
                session['user_type'] = 'nurse'
                session['first_name'] = user.first_name
                session['id'] = user.id
                session['access_id'] = self.unique_identifier_value.data
                session['selected_clinic'] = None
                session['has_selected_walk_in'] = None
                session['selected_patient'] = None
                session['selected_appointment'] = None
                return True
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('No nurse registered with that Access ID', 'danger')
        return False


class LoginPatientAuthenticator(LoginAuthenticator):
    unique_identifier_value = StringField('Email', [validators.InputRequired(), validators.Length(min=5)])
    unique_identifier = 'email'

    def authenticate_user(self, user):
        if user:
            if sha256_crypt.verify(self.password.data, user.password):
                session['logged_in'] = True
                session['user_type'] = 'patient'
                session['id'] = user.id
                session['first_name'] = user.first_name
                session['selected_clinic'] = None
                session['has_selected_walk_in'] = None
                session['newly_booked_appointment_ids'] = []
                session['selected_appointment'] = None
                return True
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('No user registered with that email address', 'danger')
        return False
