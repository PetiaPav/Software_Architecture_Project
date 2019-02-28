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
        validators.DataRequired(),
        validators.Regexp(regex="[A-Z]{4}\\d{8}")
    ])
    phone_number = StringField('Phone Number')
    birthday = DateField('Birth Date', format='%m/%d/%y')
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    physical_address = StringField('Address')


class DoctorForm(UserForm):
    permit_number = IntegerField('Permit Number',
                                 [validators.DataRequired(),
                                  validators.NumberRange(min=0, max=9999999,
                                                         message="A permit number must only have 7 digits.")
                                  ])

    specialty = StringField('Specialty')
    city = StringField('City')


class NurseForm(UserForm):
    access_id = StringField('Access id', [
        validators.DataRequired(),
        validators.Regexp(regex="[A-Z]{3}\\d{5}")
    ])


class AppointmentForm(Form):
    doctor_id = SelectField('Doctor Name', choices=[('1', 'Ivanov'), ('2', 'Petrov')])
    room = SelectField('Room Number', choices=[('1', '1'), ('2', '2')])
    # TODO will need to properly validate and convert the times
    start_time = StringField('Start Time')
    end_time = StringField('Start Time')
