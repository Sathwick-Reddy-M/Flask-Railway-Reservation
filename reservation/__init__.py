from flask import Flask, make_response, request, redirect, url_for
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt, set_access_cookies, get_jwt_identity, create_access_token, jwt_required, unset_jwt_cookies
from datetime import timedelta, datetime, timezone

from reservation.db import db

from reservation.resources import Login, Home, SignUp, LogOut, TrainDetails, Seats, Details, OTP
from reservation.blocklist import BLOCKED
from reservation.forms import LoginForm

import os


app = Flask(__name__)
app.config['BASE_URL'] = 'http://127.0.0.1:5000'
app.config['SECRET_KEY'] = 'e9cab77e2de77c4bf7117d851f3563e0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

app.config['JWT_SECRET_KEY'] = '9ec4e8d8f1a08434a04f3ce26c38f7dd'

# If true this will only allow the cookies that contain your JWTs to be sent
# over https. In production, this should always be set to True
app.config["JWT_COOKIE_SECURE"] = False

app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_CHECK_FORM'] = True

app.config["JWT_TOKEN_LOCATION"] = ['cookies']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

app.config["JWT_SESSION_COOKIE"] = False


app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('flask-mail-username')
app.config['MAIL_PASSWORD'] = os.environ.get('flask-mail-password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('flask-mail-username')
app.config['MAIL_USE_TLS'] = True

api = Api(app)
jwt = JWTManager(app)

api.add_resource(Home, '/')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(LogOut, '/logout')
api.add_resource(TrainDetails, '/search')
api.add_resource(Seats, '/seats/<train_id>/<date_time>')
api.add_resource(Details, '/details')
api.add_resource(OTP, '/otp')


@app.before_first_request
def create_tables():
    db.create_all()


@app.after_request
def refresh_tokens(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(headers, decrypted_token):
    return decrypted_token['jti'] in BLOCKED


@jwt.unauthorized_loader
def no_token(err):
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    return response


@jwt.needs_fresh_token_loader
def no_fresh_token(headers, payload):
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    return response


@jwt.revoked_token_loader
def revoked_token(headers, payload):
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    return response


@jwt.expired_token_loader
def expired_token(headers, payload):
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    return response


@jwt.invalid_token_loader
def invalid_token(headers, payload):
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    return response
