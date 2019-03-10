from flask import flash
from wtforms import Form, StringField, DateField, SelectField, IntegerField, PasswordField, validators
from wtforms.fields.html5 import EmailField


class UserForm(Form):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match.')
    ])
    confirm = PasswordField('Confirm Password')


class PatientForm(UserForm):
    email = EmailField('Email address', [
        validators.DataRequired(),
        validators.Email()
    ])

    health_card = StringField('Health Card', [
        validators.DataRequired()
        # TODO: Add validator for checking that health card is of the form 'LOUX08032317'
    ])
    phone_number = StringField('Phone Number')
    birthday = DateField('Birth Date', format='%m/%d/%y')
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    physical_address = StringField('Address')


class DoctorForm(UserForm):
    permit_number = IntegerField('Permit Number', [
        validators.DataRequired()
        # TODO: Add validator for ensuring permit number is 7 digits
    ])

    specialty = StringField('Specialty')
    city = StringField('City')


class NurseForm(UserForm):
    access_id = StringField('Access id', [
        validators.DataRequired()
        # TODO: Add validator for ensuring that access id is 3 letters followed by 5 digits (e.g. DOL96315)
    ])


class AppointmentForm(Form):
    doctor_id = SelectField('Doctor Name', choices=[('1', 'Ivanov'), ('2', 'Petrov')])
    room = SelectField('Room Number', choices=[('1', '1'), ('2', '2')])
    # TODO will need to properly validate and convert the times
    start_time = StringField('Start Time')
    end_time = StringField('Start Time')

def get_form_data(type, selected_object, request):
    if type == "patient":
        return generate_patient_form(selected_object, request)
    elif type =="doctor":
        return generate_doctor_form(selected_object, request)
    elif type == "nurse":
        return generate_nurse_form(selected_object, request)
    else:
        flash('Invalid user type passed as parameter', 'error')
        return None

def generate_patient_form(selected_object, request):
    form = PatientForm(request.form)

    form.first_name.data = selected_object.first_name
    form.last_name.data = selected_object.last_name
    form.email.data = selected_object.email
    form.health_card.data = selected_object.health_card
    form.phone_number.data = selected_object.phone_number
    form.birthday.data = selected_object.birthday
    form.gender.data = selected_object.gender
    form.physical_address.data = selected_object.physical_address

    return form

def generate_doctor_form(selected_object, request):
    form = DoctorForm(request.form)

    form.first_name.data = selected_object.first_name
    form.last_name.data = selected_object.last_name
    form.permit_number.data = selected_object.permit_number
    form.specialty.data = selected_object.specialty
    form.city.data = selected_object.city

    return form

def generate_nurse_form(selected_object, request):
    form = NurseForm(request.form)

    form.first_name.data = selected_object.first_name
    form.last_name.data = selected_object.last_name
    form.access_id.data = selected_object.access_id

    return form