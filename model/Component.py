
class Component:
    def __init__(self, model, form):
        self.model = model
        self.form = form


# User Class family can be moved to external file
class User(Component):
    def __init__(self):
        None


class Doctor(User):
    def __init__(self):
        None


class Nurse(User):
    def __init__(self):
        None


class Patient(User):
    def __init__(self):
        None


class Admin(User):
    def __init__(self):
        None


# Location Class family can be moved to external file
class Location(Component):
    def __init__(self, id):
        self.id = id


class City(Location):
    def __init__(self):
        None


class Clinic(Location):
    def __init__(self):
        None


class Room(Location):
    def __init__(self):
        None


# Appointment Class family can be moved to external file
class Appointment(Component):
    def __init__(self):
        None
