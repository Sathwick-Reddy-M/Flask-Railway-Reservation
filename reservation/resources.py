from flask import request, render_template, make_response, redirect, url_for
from flask_restful import Resource
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, get_jwt_identity, jwt_required, get_jwt
from sqlalchemy import and_, or_

from reservation.forms import LoginForm, SignUpForm, TrainSearchForm
from reservation.db import db
from reservation.models import User, Train, Compartment, Station, Route, Seat, TCSP
from reservation.pwd import bcrypt

from reservation.blocklist import BLOCKED
from datetime import datetime, timedelta

from reservation.mail import mail
from flask_mail import Message

import math
import random


class Home(Resource):
    @jwt_required(optional=True)
    def get(self):
        return make_response(render_template('home.html', is_login=(get_jwt_identity() is not None)))


class SignUp(Resource):
    @jwt_required(optional=True)
    def get(self):
        if get_jwt_identity() is not None:
            return make_response(render_template('error.html', error='You are logged in!!! Please logout to SignUp'))
        return make_response(render_template('signup.html', form=SignUpForm(), is_login=(get_jwt_identity() is not None)))

    def post(self):
        form = SignUpForm()

        if form.validate_on_submit():
            email = request.form.get('email')
            pwd = request.form.get('pwd')
            pwd_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
            age = request.form.get('age')

            user = User.query.filter((User.user_email == email)).first()

            if not user:
                otp = OTP.generate_otp()
                msg = Message('OTP Verification',
                              recipients=[email])
                msg.body = f'Your OTP: {otp}. It is valid only for 1 hour'
                mail.send(msg)

                db.session.add(
                    User(user_email=email, user_pwd=pwd_hash, user_age=age, user_verified=otp, user_verification_date=(datetime.now() + timedelta(hours=1))))
                db.session.commit()
                return make_response(render_template('verification.html', email=email))

            return make_response(render_template('error.html', error='Email taken'))

        return make_response(render_template('error.html', error='Form Validation Error'))


class Login(Resource):
    @jwt_required(optional=True)
    def get(self):
        if get_jwt_identity() is not None:
            return make_response(render_template('error.html', error='You are already logged in!!!'))
        return make_response(render_template('login.html', form=LoginForm(), is_login=(get_jwt_identity() is not None)))

    def post(self):
        form = LoginForm()

        if form.validate_on_submit():
            email = request.form.get('email')
            pwd = request.form.get('pwd')

            user = User.query.filter((User.user_email == email)).first()
            if user and bcrypt.check_password_hash(user.user_pwd, pwd) and user.user_verified == 0:
                access_token = create_access_token(
                    identity=str(user.user_id), fresh=True)
                response = make_response(
                    redirect(url_for('home')))
                set_access_cookies(response, access_token)
                return response
            return make_response(render_template('error.html', error='Invalid User Credentials (or) Email not verified'))

        return make_response(render_template('error.html', error='Form Validation Error'))


class LogOut(Resource):
    @jwt_required(optional=True)
    def get(self):
        response = make_response(render_template('home.html', is_login=False))
        if get_jwt():
            BLOCKED.add(get_jwt()['jti'])
        unset_jwt_cookies(response)
        return response


class TrainDetails(Resource):

    def get(self):
        return make_response(render_template('train_search.html', form=TrainSearchForm()))

    def post(self):
        form = TrainSearchForm()

        if form.validate_on_submit():
            start = request.form.get('start')
            destination = request.form.get('destination')
            search_date = request.form.get('searchdate')

            available_routes, avaliable_trains = self.get_available_trains_and_routes(
                start, destination, search_date)
            train_names_map = self.get_train_names_map(avaliable_trains)
            return make_response(render_template('route.html', routes=available_routes, train_names_map=train_names_map, start_station_name=start, destination_station_name=destination, search_date=search_date))
        return make_response(render_template('train_search.html', form=form))

    def get_available_trains_and_routes(self, start, destination, search_date):
        search_date = datetime.strptime(search_date, "%Y-%m-%d")

        available_trains = []
        available_routes = []

        start_station_id = Station.query.filter_by(
            station_name=start).first().station_id
        destination_station_id = Station.query.filter_by(
            station_name=destination).first().station_id

        routes = Route.query.filter(and_(Route.station_id.in_(
            [start_station_id, destination_station_id]), and_(Route.arrival_time >= search_date, Route.arrival_time < (search_date + timedelta(days=1))))).order_by(Route.train_id).all()

        for route in routes:
            if route.station_id == start_station_id:
                l = [x for x in routes if x.train_id == route.train_id and x.station_id ==
                     destination_station_id and x.depart_time > route.arrival_time]

                if l:
                    available_trains.append(route.train_id)
                    available_routes.append((route, l[0]))

        return available_routes, available_trains

    def get_train_names_map(self, train_ids):
        trains = Train.query.filter(Train.train_id.in_(train_ids)).all()
        train_names_map = {x.train_id: x.train_name for x in trains}

        return train_names_map


class Seats(Resource):
    @jwt_required()
    def get(self, train_id, date_time):
        date_time = datetime.fromisoformat(date_time)
        train_details = Train.query.filter_by(train_id=train_id).first()
        seat_details = TCSP.query.filter(and_(and_(TCSP.train_start_time >= date_time, TCSP.train_start_time < (
            date_time + timedelta(days=1))), TCSP.train_id == train_id)).order_by(TCSP.compartment_order).all()

        print(seat_details)

        return make_response(render_template('seats.html', train_details=train_details, seat_details=seat_details, csrf=get_jwt()['csrf']))

    @ jwt_required()
    def post(self, train_id, date_time):
        seats = request.form.getlist("seatSelection")
        print(seats)

        if len(seats) > 0 and len(seats) < 5:
            seat_info = []
            compartment_info = []
            for seat in seats:
                train_id, compartment_order, seat_number, *time = seat.split()
                seat_info.append(int(seat_number))
                compartment_info.append(int(compartment_order))
            train_id, compartment_order, seat_number, *time = seats[0].split()

            train_start_time = datetime.fromisoformat(' '.join(time))

            min_d = {'SL': 35, 'SU': 3, 'L': 30, 'M': 25, 'U': 3}
            if (train_start_time + timedelta(hours=5)) >= datetime.now():
                min_d = {key: 3 for key in min_d}

            return make_response(render_template('details.html', seats=seat_info, train_id=train_id, compartment_info=compartment_info, train_start_time=train_start_time, csrf=get_jwt()['csrf'], min_d=min_d))

        return 'You can only reserve 1 to 5 seats at a time'


class Details(Resource):

    @ jwt_required()
    def post(self):
        print(request.form)
        train_id = request.form['train_id']
        compartment_info = request.form['compartment_info'][1:-1].split(', ')
        seats = request.form['seat_info'][1:-1].split(', ')
        train_start_time = datetime.fromisoformat(
            request.form['train_start_time'])

        for seat_number, compartment_order in zip(seats, compartment_info):
            cur_seat = TCSP.query.filter_by(train_id=train_id, compartment_order=compartment_order,
                                            seat_number=seat_number, train_start_time=train_start_time).first()
            cur_seat.passenger_id = get_jwt_identity()
            db.session.commit()

        return 'Your Tickets have been successfully booked'


class OTP(Resource):
    def post(self):
        email = request.form.get('email')
        otp = request.form.get('otp')

        user = User.query.filter((User.user_email == email)).first()

        if user and user.user_verified != 0 and user.user_verification_date >= datetime.now():
            user.user_verified = 0
            user.user_verification_date = datetime.now()

            db.session.commit()

            return make_response(render_template('home.html', is_login=False))
        return make_response(render_template('error.html', error="Invalid OTP"))

    @ classmethod
    def generate_otp(cls):
        digits = '123456789'
        otp = ''

        for i in range(5):
            otp += digits[math.floor(random.random() * 9)]

        return otp
