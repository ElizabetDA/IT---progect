from flask_sqlalchemy import SQLAlchemy

# Создаем объект SQLAlchemy
db = SQLAlchemy()


# Cоздаем модель User для базы данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"User {self.email}"
