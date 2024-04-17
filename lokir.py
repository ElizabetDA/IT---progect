from flask import render_template, request, \
    jsonify, make_response, redirect, url_for
from models import db, User, Trip
from forms import RegistrationForm, LoginForm, TripForm
from sqlalchemy.orm.exc import NoResultFound
import hashlib
from flask_jwt_extended import create_access_token, \
    jwt_required, get_jwt_identity


# Функция получения домашней страницы
def register_routes(app):
    @app.route("/")
    def index():
        return "<h1> Hello </h1>"

    # Функция регистрации
    @app.route("/register", methods=["POST"])
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
            return jsonify({"message": "Пользователь успешно зарегистрирован"}), 200

        # Возвращение подсказок пользователю
        return make_response(render_template("register.html", form=form), 400)

    # Функция получения формы регистрации
    @app.route("/register", methods=["GET"])
    def registrationForm():
        form = RegistrationForm()
        return render_template("register.html", form=form)

    # Функция авторизации
    @app.route("/login", methods=["POST"])
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
                    response = make_response(redirect(url_for("order_get")))
                    response.set_cookie("access_token_cookie", value=access_token)
                    return response
                else:
                    return jsonify({"message": "Неверный пароль"}), 401
            except NoResultFound:
                return jsonify({"message": "Пользователь не найден"}), 404
        # Возвращение подсказок пользователю
        return make_response(render_template("login.html", form=form), 400)

    # Функция получения формы авторизации
    @app.route("/login", methods=["GET"])
    def authorizationForm():
        form = LoginForm()
        return render_template("login.html", form=form)

    # Функция получения формы для заказа
    @app.route("/order", methods=["GET"])
    @jwt_required()
    def order_get():
        form = TripForm()
        return render_template("order.html", form=form)

    # Функция создания заказа
    @app.route("/order", methods=["POST"])
    @jwt_required()
    def order_create():
        form = TripForm(request.form)
        if form.validate_on_submit() is True:
            pickup_location = form.pickup_location.data
            dropoff_location = form.dropoff_location.data
            user_id = get_jwt_identity()
            fare = Trip.calculate_fare(pickup_location, dropoff_location)
            new_trip = Trip(pickup_location=pickup_location,
                            dropoff_location=dropoff_location,
                            user_id=user_id,
                            fare=fare,
                            status="В ожидании")
            db.session.add(new_trip)
            db.session.commit()
            print(pickup_location)
            print(dropoff_location)
            return jsonify({"message": "Заказ успешно создан"}), 200
        return make_response(render_template("order.html", form=form), 400)
