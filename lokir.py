from flask import render_template, request, \
                  jsonify, make_response, redirect, url_for
from models import db, User
from forms import RegistrationForm, LoginForm, TripForm
from sqlalchemy.orm.exc import NoResultFound
import hashlib
from flask_jwt_extended import create_access_token, \
                               jwt_required


# Функция получения домашней страницы
def index():
    return "<h1> Hello </h1>"


# Функция регистрации
def registration():
    form = RegistrationForm(request.form)
    # Валидация
    if form.validate_on_submit() is True:
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        print(username, email, password_hash)
        if User.query.filter_by(email=email).first():
            return (
                jsonify(
                    {
                        "message": "Пользователь с таким \
                            адресом электронной почты уже существует"
                    }
                ),
                409,
            )

        new_user = User(username=username, email=email,
                        password_hash=password_hash)
        # Добавляем пользователя в БД
        db.session.add(new_user)
        db.session.commit()
        # Все успешно
        return (jsonify({"message": "Пользователь успешно зарегистрирован"}),)
    200
    # Возвращение подсказок пользователю
    return make_response(render_template("register.html", form=form), 400)


# Функция получения формы регистрации
def registrationForm():
    form = RegistrationForm()
    return render_template("register.html", form=form)


# Функция авторизации
def authorization():
    form = LoginForm(request.form)
    # Валидация
    if form.validate_on_submit() is True:
        try:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).one()
            # Сравниваем хэш введенного пароля с
            # хэшем пароля найденного пользователя
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == user.password_hash:
                # Создание токена и переход на страницу создания заказа
                # для уже авторизованного пользователя
                access_token = create_access_token(identity=user.id)
                response = make_response(redirect(url_for(".lokir_order_get")))
                response.set_cookie("access_token_cookie", value=access_token)
                return response
            else:
                return jsonify({"message": "Неверный пароль"}), 401
        except NoResultFound:
            return jsonify({"message": "Пользователь не найден"}), 404
    # Возвращение подсказок пользователю
    return make_response(render_template("login.html", form=form), 400)


# Функция получения формы авторизации
def authorizationForm():
    form = LoginForm()
    return render_template("login.html", form=form)


# Функция получения формы для заказа
@jwt_required()
def order_get():
    form = TripForm()
    return render_template("order.html", form=form)


# Функция создания заказа
@jwt_required()
def order_create():
    form = TripForm(request.form)
    if form.validate_on_submit() is True:
        pickup_location = form.pickup_location.data
        dropoff_location = form.dropoff_location.data
        print(pickup_location)
        print(dropoff_location)
    return make_response(render_template("order.html", form=form), 400)
