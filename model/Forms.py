from datetime import datetime
import re, json

from dateutil import relativedelta
from flask import flash
from wtforms import Form, StringField, DateField, SelectField, IntegerField, PasswordField, validators, ValidationError, SelectMultipleField
from wtforms.fields.html5 import EmailField




def alpha(minimum, maximum, allow_digits):
    def _alpha(form, field):
        length = len(field.data)
        if length < minimum or length > maximum:
            raise ValidationError('Input length must be between %d and %d characters long.' % (minimum, maximum))
        if allow_digits == 0:
            if any(char.isdigit() for char in field.data):
                raise ValidationError('Input must not contain any digits.')
    return _alpha


def password(form, field):
    minimum_password_length = 6
    if type(field.data) is str:
        if not any(char.isdigit() for char in field.data):
            raise ValidationError('Password must contain at least 1 digit.')
        elif not any(char.isalpha() for char in field.data):
            raise ValidationError('Password must contain at least 1 letter.')
    elif len(field.data) < minimum_password_length:
        raise ValidationError('The password needs to be at least ' + str(minimum_password_length) + ' characters.')


def phone_number(form, field):
    if len(field.data) == 0:
        raise ValidationError('Please enter a phone number.')
    elif not re.match('^[(]\d{3}[)]\s*\d{3}[-]\d{4}$', field.data):
        raise ValidationError('Invalid phone number, please follow the pattern: (514) 423-3918')


def health_card(form, field):
    if len(field.data) == 0:
        raise ValidationError('Please enter a health card number.')
    elif not re.match('^[a-zA-Z]{4}\s*\d{4}\s*\d{4}$', field.data):
        raise ValidationError('Invalid health card number, please follow the pattern: LOUX 0803 2317.')


def permit_number(form, field):
    if field.data == '' or not all(char.isdigit() for char in field.data):
        raise ValidationError('Input must be a valid digit.')
    data = int(field.data)
    if data < 1000000 or data > 9999999:
        raise ValidationError('Please enter a valid 7-digit licence number.')


def nurse_access(form, field):
    if len(field.data) == 0:
        raise ValidationError('Please enter a nurse access id number.')
    elif not re.match('^[a-zA-Z]{3}\s*\d{5}$', field.data):
        raise ValidationError('Invalid access id number, please follow the pattern: DOL96315.')

def room_valid(form, field):
    if field.data == '' or not all(char.isdigit() for char in field.data):
        raise ValidationError('Input must be a valid digit.')
    data = int(field.data)
    if data < 0 or data > 100:
        raise ValidationError('Please enter a number of rooms between 0 and 100')


def is_adult(form, field):
    age = relativedelta.relativedelta(datetime.now(), field.data)
    if age.years < 18:
        raise ValidationError('Patient must be at least 18 years old.')


class UserForm(Form):
    first_name = StringField('First Name', [alpha(2, 50, 0)])
    last_name = StringField('Last Name', [alpha(2, 50, 0)])
    password = PasswordField('Password', [
        password,
        validators.EqualTo('confirm', message='Passwords do not match.')
    ])
    confirm = PasswordField('Confirm Password')


class PatientForm(UserForm):
    email = EmailField('Email address', [validators.Email()])
    health_card = StringField('Health Card', [health_card])
    phone_number = StringField('Phone Number', [phone_number])
    birthday = DateField('Birth Date', [is_adult], format='%d/%m/%Y')
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    physical_address = StringField('Address', [alpha(2, 100, 1)])


class DoctorForm(UserForm):
    permit_number = StringField('Permit Number', [permit_number])
    specialty = StringField('Specialty', [alpha(2, 50, 0)])
    city = StringField('City', [alpha(2, 50, 0)])


class NurseForm(UserForm):
    access_id = StringField('Access id', [nurse_access])

def _add_chosen_class(kwargs):
    if 'render_kw' in kwargs:
        if 'class' in kwargs['render_kw']:
            kwargs['render_kw']['class'] += ' chosen-select'
        else:
            kwargs['render_kw']['class'] = 'chosen-select'
    else:
        kwargs['render_kw'] = {'class': 'chosen-select'}


class ChosenSelectField(SelectField):
    def __init__(self, *args, **kwargs):
        _add_chosen_class(kwargs)
        super(ChosenSelectField, self).__init__(*args, **kwargs)


class ChosenSelectMultipleField(SelectMultipleField):
    def __init__(self, *args, **kwargs):
        _add_chosen_class(kwargs)
        super(ChosenSelectMultipleField, self).__init__(*args, **kwargs)


class ClinicForm(Form):
    name = StringField('Name', [validators.required()])
    physical_address = StringField('Physical Address', [validators.required()])
    start_time = StringField('Opening Time', default = "09:00", validators=[
        validators.required(),
        validators.regexp(regex="(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])", message="Please input a valid time in the correct format, Example: 11:00")])
    end_time = StringField('Closing Time', default = "17:00", validators=[
        validators.required(),
        validators.regexp(regex="(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])", message="Please input a valid time in the correct format, Example: 11:00")])
    rooms = StringField('Number of Rooms', [validators.required(), room_valid])
    doctors = ChosenSelectMultipleField("Doctors", coerce=int)
    nurses = ChosenSelectMultipleField("Nurses", coerce=int)


def get_form_data(type, selected_object, request):
    if type == "patient":
        return generate_patient_form(selected_object, request)
    elif type == "doctor":
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
