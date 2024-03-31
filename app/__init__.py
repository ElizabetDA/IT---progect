from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
# Импортируем маршруты
from . import routes

# Создаем базу данных, если она еще не была создана
with app.app_context():
    db.create_all()
