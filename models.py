from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
import hashlib
import math

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    trips = db.relationship("Trip", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"User {self.email}"

    def changePassword(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()


class Trip(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"),
                          nullable=True)
    pickup_location = db.Column(db.String(200), nullable=False)
    dropoff_location = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime,
                           nullable=False, default=datetime.
                           now(pytz.timezone("Europe/Moscow")))
    end_time = db.Column(db.DateTime, nullable=True)
    fare = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="В ожидании")
    len_way = db.Column(db.String(50), nullable=False)

    def changeStatus(self, status):
        self.status = status

    def chandeDriverId(self, driver_id):
        self.driver_id = driver_id

    def __repr__(self):
        return (f"Trip {self.id} - User: {self.user.username},"
                f"Driver: {self.driver.name if self.driver else None}, \
                Status: {self.status}")

    def calculateFare(lenWay):
        return math.ceil(lenWay * 0.02 + 100)

    def setCompleted(self):
        self.status = "Завершен"
        self.end_time = datetime.now(pytz.timezone("Europe/Moscow"))


class Driver(db.Model):
    __tablename__ = "drivers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    car_model = db.Column(db.String(100), nullable=False)
    license_plate = db.Column(db.String(20), nullable=False)
    availability = db.Column(db.String(100), nullable=False,
                             default="Свободен")
    location = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    trips = db.relationship("Trip", backref="driver", lazy="dynamic")

    def changeAvailability(self, availability):
        self.availability = availability

    def addMoneyForTrip(self, fare):
        self.balance += fare

    def __repr__(self):
        return f"Driver {self.name}, Car {self.car_model}, \
    Phone: {self.phone_number}"
