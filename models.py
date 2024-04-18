from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

# Создаем объект SQLAlchemy
db = SQLAlchemy()


# Cоздаем модель User для базы данных
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"User {self.email}"


# Cоздаем модель Order для базы данных
class Trip(db.Model):
    __tablename__ = "trips"
    trip_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    driver_id = db.Column(db.Integer,
                          db.ForeignKey("drivers.driver_id"), nullable=True)
    pickup_location = db.Column(db.String(200), nullable=False)
    dropoff_location = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime,
                           nullable=False, default=datetime.
                           now(pytz.timezone("Europe/Moscow")))
    end_time = db.Column(db.DateTime, nullable=True)
    fare = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    # Определяем отношение между таблицами Order и User
    user = db.relationship("User", backref="orders")

    # Определяем отношение между таблицами Order и Driver
    driver = db.relationship("Driver", backref="orders")

    def __repr__(self):
        return f"Order {self.trip_id} - User: \
    {self.user_id}, Driver: {self.driver_id}, Status: {self.status}"

    @staticmethod
    def calculate_fare(pickup_location, dropoff_location):
        return 1000

    def set_completed(self):
        self.status = "Завершен"
        self.end_time = datetime.now(pytz.timezone("Europe/Moscow"))


# Cоздаем модель Driver для базы данных
class Driver(db.Model):
    __tablename__ = "drivers"
    driver_id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    car_model = db.Column(db.String(100), nullable=False)
    car_license_plate = db.Column(db.String(20), nullable=False)
    availability = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Driver {self.driver_name}, Car \
    {self.car_model}, Phone: {self.phone_number}"
