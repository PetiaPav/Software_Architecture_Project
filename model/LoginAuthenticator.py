from wtforms import Form, PasswordField, validators, StringField
from flask import session, flash
from passlib.hash import sha256_crypt


class LoginAuthenticator(Form):
    password = PasswordField('Password', [validators.Length(min=6)])


class LoginDoctorAuthenticator(LoginAuthenticator):
    permit_number = StringField('Physician Permit Number', [validators.Length(min=7)])

    def authenticate_user(self, tdg):
        user = tdg.get_doctor_by_permit_number(self.permit_number.data)
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


class LoginNurseAuthenticator(LoginAuthenticator):
    access_id = StringField('Access ID', [validators.Length(min=8)])

    def authenticate_user(self, tdg):
        user = tdg.get_nurse_by_access_id(self.access_id.data)
        if user:
            if sha256_crypt.verify(self.password.data, user["password"]):
                session['logged_in'] = True
                session['user_type'] = 'nurse'
                session['first_name'] = user['first_name']
                session['id'] = user['id']
                session['access_id'] = self.access_id.data
                session['selected_clinic'] = None
                session['has_selected_walk_in'] = None
                return True
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('No nurse registered with that Access ID', 'danger')
        return False


class LoginPatientAuthenticator(LoginAuthenticator):
    email = StringField('Email', [validators.InputRequired(), validators.Length(min=5)])

    def authenticate_user(self, tdg):
        user = tdg.get_patient_by_email(self.email.data)
        if user:
            if sha256_crypt.verify(self.password.data, user["password"]):
                session['logged_in'] = True
                session['user_type'] = 'patient'
                session['id'] = user['id']
                session['first_name'] = user['first_name']
                session['id'] = user['id']
                session['selected_clinic'] = None
                session['has_selected_walk_in'] = None
                return True
            else:
                flash('Incorrect password', 'danger')
        else:
            flash('No user registered with that email address', 'danger')
        return False
