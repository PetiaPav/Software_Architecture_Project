from flask import session

def test_reg_patient(client):
    data = dict([('email', 'ivan@mail.ru'), ('password', 'q1w2e3'), ('confirm', 'q1w2e3'), ('first_name', 'Ivan'),
                 ('last_name', 'Ivanov'), ('health_card', 'IVAN 1234 0987'), ('phone_number', '(123) 456-7890'),
                 ('birthday', '01/01/80'), ('gender', 'M'), ('physical_address', '123 Main Street')])
    rv = client.post('/register/patient', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'You are now registered and can log in!' in rv.data


def test_login_patient(client):
    data = dict([('email', 'ivan@mail.ru'), ('password', 'q1w2e3')])
    rv = client.post('/login/patient', data=data, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Hello Ivan, Welcome' in rv.data
    assert session['logged_in'] is True

    rv2 = client.get('/logout', follow_redirects=True)
    assert rv2.status_code == 200
    assert b'You are now logged out!' in rv2.data
