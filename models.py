from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz, hashlib

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

    def change_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()


class Trip(db.Model):
    __tablename__ = "trips"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=True)
    pickup_location = db.Column(db.String(200), nullable=False)
    dropoff_location = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Europe/Moscow')))
    end_time = db.Column(db.DateTime, nullable=True)
    fare = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="В ожидании")

    def __repr__(self):
        return f"Trip {self.id} - User: {self.user.username}, Driver: {self.driver.name if self.driver else None}, Status: {self.status}"

    @staticmethod
    def calculate_fare(pickup_location, dropoff_location):
        return 1000

    def set_completed(self):
        self.status = "Завершен"
        self.end_time = datetime.now(pytz.timezone('Europe/Moscow'))


class Driver(db.Model):
    __tablename__ = "drivers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    car_model = db.Column(db.String(100), nullable=False)
    license_plate = db.Column(db.String(20), nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    location = db.Column(db.String(100), nullable=False)
    trips = db.relationship("Trip", backref="driver", lazy="dynamic")

    def __repr__(self):
        return f"Driver {self.name}, Car {self.car_model}, Phone: {self.phone_number}"
