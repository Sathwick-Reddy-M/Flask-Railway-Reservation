from reservation.db import db


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(80), nullable=False, unique=True)
    user_pwd = db.Column(db.String(80), nullable=False)
    user_age = db.Column(db.Integer)
    user_verified = db.Column(db.Integer, nullable=False)
    user_verification_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_email, user_pwd, user_age, user_verified, user_verification_date):
        self.user_email = user_email
        self.user_pwd = user_pwd
        self.user_age = user_age
        self.user_verified = user_verified
        self.user_verification_date = user_verification_date

    def __repr__(self):
        return f'{self.user_id}, {self.user_email}'

# Assumed that in every compartment the seat numbering starts from 1 to compartment_capacity


class Train(db.Model):
    __tablename__ = 'trains'

    train_id = db.Column(db.String(10), primary_key=True)
    train_name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{self.train_id}, {self.train_name}'


class Compartment(db.Model):
    __tablename__ = 'compartments'

    compartment_id = db.Column(db.String(10), primary_key=True)
    compartment_type = db.Column(db.String(20), unique=True)
    compartment_capacity = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.compartment_id}, {self.compartment_type}, {self.compartment_capacity}'


class Seat(db.Model):
    __tablename__ = 'seats'

    seat_id = db.Column(db.String(10), primary_key=True)
    seat_status = db.Column(db.String(20), nullable=False)
    seat_type = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'{self.seat_id}, {self.seat_status}, {self.seat_type}'


class TCSP(db.Model):
    train_id = db.Column(db.String(10), db.ForeignKey(
        'trains.train_id'), nullable=False, primary_key=True)
    compartment_id = db.Column(db.String(10), db.ForeignKey(
        'compartments.compartment_id'), nullable=False, primary_key=True)
    compartment_order = db.Column(db.Integer, nullable=False, primary_key=True)
    seat_id = db.Column(db.String(10), db.ForeignKey(
        'seats.seat_id'), nullable=False, primary_key=True)
    seat_number = db.Column(db.Integer, nullable=False, primary_key=True)
    passenger_id = db.Column(db.String(10), db.ForeignKey(
        'users.user_id'), nullable=True, default=None)
    train_start_time = db.Column(db.DateTime, nullable=False, primary_key=True)

    def __repr__(self):
        return f'{self.train_id}, {self.compartment_id}, {self.compartment_order}, {self.seat_id}, {self.seat_number}, {self.passenger_id}, {self.train_start_time}'


class Station(db.Model):
    __tablename__ = 'stations'

    station_id = db.Column(db.String(10), primary_key=True)
    station_name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'{self.station_id}, {self.station_name}'


class Route(db.Model):
    __tablename__ = 'routes'

    train_id = db.Column(db.String(10), db.ForeignKey(
        'trains.train_id'), nullable=False, primary_key=True)
    station_id = db.Column(db.String(10), db.ForeignKey(
        'stations.station_id'), nullable=False, primary_key=True)
    arrival_time = db.Column(db.DateTime, primary_key=True)
    depart_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'{self.train_id}, {self.station_id}, {self.arrival_time}, {self.depart_time}'
