from flask import render_template, redirect, url_for, flash, request, jsonify
from run import app, db
from models import User
from forms import RegistrationForm, LoginForm
from sqlalchemy.orm.exc import NoResultFound
import hashlib


@app.route("/")
def index():
    return f"<h1> Hello <h1>"


# Функция регистрации
def registration():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username or not email or not password:
        return jsonify({"message": "Неверный формат данных"}), 400
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    print(username, email, password_hash)
    if User.query.filter_by(email=email).first():
        return (
            jsonify(
                {
                    "message": "Пользователь с таким адресом \
            электронной почты уже существует"
                }
            ),
            409,
        )
    new_user = User(username=username, email=email,
                    password_hash=password_hash)
    # Добавляем пользователя в БД
    db.session.add(new_user)
    db.session.commit()
    # Все успешно, код 200
    return jsonify({"message": "Пользователь успешно зарегистрирован"}), 200


def registrationForm():
    return render_template("index.html")


# Функция авторизации
def authorization():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "Необходимо адрес \
                        электронной почты и пароль"}), 400
    try:
        # Находим пользователя в БД по email.
        # Метод one() выдаст исключение Noresultfound в случае,
        # если результатов нет
        user = User.query.filter_by(email=email).one()
        # Сравниваем хэш введенного пароля с
        # хэшем пароля найденного пользователя (код 200)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash == user.password_hash:
            return jsonify({"message": "Успешная авторизация"}), 200
        else:
            return jsonify({"message": "Неверный пароль"}), 401
    except NoResultFound:
        return jsonify({"message": "Пользователь не найден"}), 404


def authorizationForm():
    return render_template("login.html")
