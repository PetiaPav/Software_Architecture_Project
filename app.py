from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from model.Tdg import Tdg
from model.Forms import RegisterForm
from passlib.hash import sha256_crypt


app = Flask(__name__)
tdg = Tdg(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
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


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)
