import re
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bidboard import db, app
from bidboard.helpers.helpers import validation_preparation
import re
import datetime
import jwt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(64),
                             unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text)
    successful_bookings = db.Column(db.ARRAY(db.Integer), nullable=True)    
    media = db.relationship("Medium", backref="users", lazy=True,
                             order_by="desc(Medium.id)", cascade="delete, delete-orphan")
    bids = db.relationship("Bid", backref="users",
                             order_by="desc(Bid.id)", cascade="delete, delete-orphan")

    def __init__(self, company_name, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.company_name = company_name
        self.set_password(password)
        self.successful_bookings = []

    def __repr__(self):
        return f"{self.company_name} with email {self.email} saved to database!"

    @validates('first_name')
    @validation_preparation
    def validate_first_name(self, key, first_name):
        if not first_name:
            self.validation_errors.append('No First Name provided')

        return first_name

    @validates('last_name')
    @validation_preparation
    def validate_last_name(self, key, last_name):
        if not last_name:
            self.validation_errors.append('No Last Name provided')

        return last_name

    @validates('company_name')
    @validation_preparation
    def validate_company_name(self, key, company_name):
        if not company_name:
            self.validation_errors.append('No Company Name provided')

        if (not self.company_name == company_name):
            if User.query.filter_by(company_name=company_name).first():
                self.validation_errors.append('Company Name is already in use')

        if len(company_name) > 0 and (len(company_name) < 3 or len(company_name) > 50):
            self.validation_errors.append(
                'Company Name must be between 3 and 50 characters')

        return company_name

    @validates('email')
    @validation_preparation
    def validate_email(self, key, email):
        if not email:
            self.validation_errors.append('No email provided')

        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            self.validation_errors.append(
                'Provided email is not an email address')

        if (not self.email == email):
            if User.query.filter_by(email=email).first():
                self.validation_errors.append('Email is already in use')

        return email

    def set_password(self, password):
        if not password:
            self.validation_errors.append('Password not provided')

        if len(password) > 0 and (len(password) < 8 or len(password) > 50):
            self.validation_errors.append(
                'Password must be between 8 and 50 characters')

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_successful_bookings(self):
        bids = self.bids
        successful_bookings = []
        for bid in bids:
            if bid.is_confirmed:
                successful_bookings.append(bid.id)
        self.successful_bookings = successful_bookings
        return successful_bookings


    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 0
        except jwt.InvalidTokenError:
            return 0
