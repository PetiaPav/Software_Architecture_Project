from wtforms import Form, StringField, DateField, SelectField, TextAreaField, PasswordField, validators


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


class AppointmentForm(Form):
    doctor_id = SelectField('Doctor Name', choices=[('1', 'Ivanov'), ('2', 'Petrov')])
    room = SelectField('Room Number', choices=[('1', '1'), ('2', '2')])
    # TODO will need to properly validate and convert the times
    start_time = StringField('Start Time')
    end_time = StringField('Start Time')

