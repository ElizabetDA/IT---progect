from flask import render_template, request, \
    jsonify, make_response, redirect, url_for
from models import db, User, Trip
from forms import RegistrationForm, LoginForm, TripForm, ChangePasswordForm
from sqlalchemy.orm.exc import NoResultFound
import hashlib
from flask_jwt_extended import create_access_token, \
    jwt_required, get_jwt_identity, create_refresh_token


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
            return jsonify({"message":
                            "Пользователь успешно зарегистрирован"}), 200

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
                    refresh_token = create_refresh_token(identity=user.id)
                    response = make_response(redirect(url_for("order_get")))
                    response.set_cookie("refresh_token_cookie",
                                        value=refresh_token,
                                        httponly=True, secure=True)
                    response.set_cookie("access_token_cookie",
                                        value=access_token)
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
        # Возвращение подсказок пользователю
        return make_response(render_template("order.html", form=form), 400)


    @app.route("/account", methods=["GET"])
    @jwt_required()
    def account():
        # Получаем идентификатор авторизованного пользователя из JWT токена
        user_id = get_jwt_identity()

        # Извлекаем объект пользователя из базы данных по его идентификатору
        user = User.query.get(user_id)

        # Получаем заказы пользователя из связанной коллекции
        user_trips = user.trips

        # Рендерим шаблон account.html и передаем в него данные пользователя и его заказы
        return render_template("account.html", user=user, trips=user_trips)

    @app.route("/logout", methods=["GET"])
    @jwt_required()
    def logout():
        # Создаем объект ответа, перенаправляющий пользователя на главную страницу
        response = make_response(redirect(url_for("index")))

        # Удаляем cookie с JWT токеном доступа, завершая сеанс пользователя
        response.delete_cookie("access_token_cookie")

        return response

    @app.route("/change_password", methods=["GET"])
    @jwt_required()
    def change_password_get():
        form = ChangePasswordForm()

        # Рендерим шаблон change_password.html и передаем в него форму
        return render_template("change_password.html", form=form)

    @app.route("/change_password", methods=["POST"])
    @jwt_required()
    def change_password():
        form = ChangePasswordForm(request.form)
        if form.validate_on_submit():
            # Получаем идентификатор авторизованного пользователя из JWT токена
            user_id = get_jwt_identity()

            # Извлекаем объект пользователя из базы данных по его идентификатору
            user = User.query.get(user_id)

            # Хешируем старый пароль из формы
            old_password_hash = hashlib.sha256(form.old_password.data.encode()).hexdigest()

            if old_password_hash != user.password_hash:
                return jsonify({'message': 'Текущий пароль неверный'}), 400

            # Устанавливаем новый пароль для пользователя
            user.change_password(form.new_password.data)

            # Добавляем измененного пользователя в сессию базы данных
            db.session.add(user)

            # Сохраняем изменения в базе данных
            db.session.commit()

            return jsonify({'message': 'Пароль успешно изменен'}), 200

    # Функция обновления access_token
    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh_token():
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        response = make_response(redirect(url_for("order_get")))
        response.set_cookie("access_token_cookie",
                            value=new_access_token)
        return response

