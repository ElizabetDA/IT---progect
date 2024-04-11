from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Создаем объект SQLAlchemy
db = SQLAlchemy()


# Cоздаем модель User для базы данных
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"User {self.email}"


# Cоздаем модель Order для базы данных
class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=True)
    pickup_location = db.Column(db.String(200), nullable=False)
    dropoff_location = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    fare = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    # Определяем отношение между таблицами Order и User
    user = db.relationship('User', backref='orders')

    # Определяем отношение между таблицами Order и Driver
    driver = db.relationship('Driver', backref='orders')

    def __repr__(self):
        return f"Order {self.trip_id} - User: {self.user_id}, Driver: {self.driver_id}, Status: {self.status}"


# Cоздаем модель Driver для базы данных
class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    car = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Driver {self.name}, Car {self.car}"
