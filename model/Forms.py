from wtforms import Form, StringField, DateField, SelectField, TextAreaField, PasswordField, validators

def valid_access_id (form, field):


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
    password = PasswordField('Password', [Length(min=6)])


class LoginDoctorForm(LoginForm):
    physician_permit_number = StringField('Physician Permit Number', Length=7)


class LoginNurseForm(LoginForm):
    access_id = StringField('Access ID', Length=8, valid_access_id)


class LoginPatientForm(LoginForm):
    email = StringField('Email', InputRequired())


class AppointmentForm(Form):
    doctor_id = SelectField('Doctor Name', choices=[('1', 'Ivanov'), ('2', 'Petrov')])
    room = SelectField('Room Number', choices=[('1', '1'), ('2', '2')])
    # TODO will need to properly validate and convert the times
    start_time = StringField('Start Time')
    end_time = StringField('Start Time')
