import os

from flask import session

def test_reg_patient(client):
    data = dict([('email', 'ivan@mail.ru'), ('password', 'q1w2e3'), ('confirm', 'q1w2e3'), ('first_name', 'Ivan'),
                 ('last_name', 'Ivanov'), ('health_card', 'IVAN 1234 0987'), ('phone_number', '(123) 456-7890'),
                 ('birthday', '01/01/1980'), ('gender', 'M'), ('physical_address', '123 Main Street')])
    rv = client.post('/register/patient', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'You are now registered and can log in!' in rv.data

def test_dup_patient(client):
    data = dict([('email', 'ivan@mail.ru'), ('password', 'q1w2e3'), ('confirm', 'q1w2e3'), ('first_name', 'Ivan'),
                 ('last_name', 'Ivanov'), ('health_card', 'IVAN 1234 0987'), ('phone_number', '(123) 456-7890'),
                 ('birthday', '01/01/1980'), ('gender', 'M'), ('physical_address', '123 Main Street')])
    rv = client.post('/register/patient', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'This e-mail address has already been registered.' in rv.data


def test_login_patient(client):
    data = dict([('password', 'q1w2e3'), ('unique_identifier_value', 'ivan@mail.ru')])
    rv = client.post('/login/patient', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Hello Ivan, Welcome' in rv.data
    assert session['logged_in'] is True

    rv2 = client.get('/logout', follow_redirects=True)
    assert rv2.status_code == 200
    assert b'You are now logged out!' in rv2.data
    assert 'logged in' not in session


def test_reg_nurse(client):
    data = dict([ ('password', '1q2w3e'), ('confirm', '1q2w3e'), ('first_name', 'Ivana'),
                 ('last_name', 'Ivanova'), ('access_id', 'CBA12345')])
    rv = client.post('/register/nurse', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'You are now registered and can log in!' in rv.data


def test_login_nurse(client):
    data = dict([('unique_identifier_value', 'CBA12345'), ('password', '1q2w3e')])
    rv = client.post('/login/nurse', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Hello Ivana, Welcome' in rv.data
    assert session['logged_in'] is True

    rv2 = client.get('/logout', follow_redirects=True)
    assert rv2.status_code == 200
    assert b'You are now logged out!' in rv2.data
    assert 'logged in' not in session


def test_reg_doctor(client):
    data = dict([ ('password', 'q1w2e3'), ('confirm', 'q1w2e3'), ('first_name', 'Peter'),
                  ('last_name', 'Petrov'), ('permit_number', '1245789'),
                  ('specialty', 'GP'), ('city', 'Montreal')])
    rv = client.post('/register/doctor', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'You are now registered and can log in!' in rv.data


def test_login_doctor(client):
    data = dict([('unique_identifier_value', '1245789'), ('password', 'q1w2e3')])
    rv = client.post('/login/doctor', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Hello Dr. Peter, Welcome' in rv.data
    assert session['logged_in'] is True

    rv2 = client.get('/logout', follow_redirects=True)
    assert rv2.status_code == 200
    assert b'You are now logged out!' in rv2.data
    assert 'logged in' not in session


def test_incorrect_patient_email(client):
    data = dict([('unique_identifier_value', 'fedor@mail.ru'), ('password', 'q1w2e3')])
    rv = client.post('/login/patient', data=data, follow_redirects=True)
    assert rv.status_code == 200
    print(rv.data)
    assert b'No user registered with that email address' in rv.data
    assert 'logged in' not in session


def test_incorrect_patient_password(client):
    data = dict([('unique_identifier_value', 'ivan@mail.ru'), ('password', 'letmein')])
    rv = client.post('/login/patient', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Incorrect password' in rv.data
    assert 'logged in' not in session


def test_reset_database():
    os.chdir('scripts')
    os.system('reset_database.py test')

