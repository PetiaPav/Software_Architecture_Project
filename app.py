from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from model.Tdg import Tdg
from model.Forms import RegisterForm
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
    email = form.email.data
    password=sha256_crypt.hash(str(form.password.data))
    first_name = form.first_name.data
    last_name = form.first_name.data
    health_card = form.health_card.data
    phone_number = form.phone_number.data
    birthday = form.birthday.data
    gender = form.gender.data
    physical_address = form.physical_address.data
    if request.method == 'POST' and form.validate():
        tdg.insert_patient(email, password, first_name, last_name, health_card, phone_number, birthday, gender, physical_address)
        flash('You are now registered and can log in!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # TODO as above.
    if request.method == 'POST':
        form = RegisterForm(request.form)
        email = form.email.data
        password_candidate = form.password.data
        user = tdg.get_patient_by_email(email)
        if user:
            if sha256_crypt.verify(password_candidate, user['password']):
                session['logged_in'] = True
                session['email'] = user['email']
                session['first_name'] = user['first_name']
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
def logout():
    session.clear()
    flash('You are now logged out!', 'success')
    return redirect(url_for('home'))


@app.route('/patient_dashboard')
@is_logged_in
def patient_dashboard():
    return render_template('patient_dashboard.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
