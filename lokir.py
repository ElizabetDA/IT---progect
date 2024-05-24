from flask import render_template, request, \
    jsonify, make_response, redirect, url_for
from models import db, User, Trip, Driver
from forms import RegistrationForm, LoginForm, TripForm, \
    ChangePasswordForm, PassageForm, ForScore
from sqlalchemy.orm.exc import NoResultFound
from flask_wtf import FlaskForm
import hashlib
from flask_jwt_extended import create_access_token, \
    jwt_required, get_jwt_identity, create_refresh_token, get_jwt
from jwtCheck import driver_required, client_required
from api import lenWay


# Функция получения домашней страницы
def register_routes(app):
    @app.route("/")
    def index():
        return render_template("home.html")

    @app.route("/about_us", methods=["GET"])
    def about_us():
        return render_template("about_us.html")

    @app.route("/information", methods=["GET"])
    def information():
        return render_template("information.html")

    @app.route("/contacts", methods=["GET"])
    def contacts():
        return render_template("contacts.html")

    @app.route("/qa", methods=["GET"])
    def qa():
        return render_template("qa.html")

    @app.route("/pricing", methods=["GET"])
    def pricing():
        return render_template("pricing.html")

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
                    access_token = create_access_token(identity=user.id,
                                                       additional_claims={
                                                           "client": True})
                    refresh_token = create_refresh_token(identity=user.id,
                                                         additional_claims={
                                                             "client": True})
                    response = make_response(redirect(url_for("orderGet")))
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
    @client_required()
    def orderGet():
        form = TripForm()
        return render_template("order.html", form=form)

    # Функция создания заказа
    @app.route("/order", methods=["POST"])
    @client_required()
    def orderCreate():
        form = TripForm(request.form)
        if form.validate_on_submit() is True:
            pickup_location = form.pickup_location.data
            dropoff_location = form.dropoff_location.data
            user_id = get_jwt_identity()
            len_way = lenWay(pickup_location, dropoff_location)
            fare = Trip.calculateFare(len_way)
            payment_method = form.payment_method.data
            new_trip = Trip(pickup_location=pickup_location,
                            dropoff_location=dropoff_location,
                            payment_method=payment_method,
                            user_id=user_id,
                            fare=fare,
                            status="В ожидании", len_way=len_way,
                            )
            db.session.add(new_trip)
            db.session.commit()
            print(pickup_location)
            print(dropoff_location)
            return jsonify({"message": "Заказ успешно создан"}), 200
        # Возвращение подсказок пользователю
        return make_response(render_template("order.html", form=form), 400)

    @app.route("/account", methods=["GET"])
    @client_required()
    def accountGet():
        # Получаем идентификатор авторизованного пользователя из JWT токена
        user_id = get_jwt_identity()

        # Извлекаем объект пользователя из базы данных по его идентификатору
        user = User.query.get(user_id)
        # Получаем заказы пользователя из связанной коллекции
        user_trips = user.trips
        form = ForScore()
        # Рендерим шаблон account.html и передаем
        # в него данные пользователя и его заказы
        return render_template("account.html", user=user,
                               trips=user_trips, form=form)

    @app.route("/account", methods=["POST"])
    @client_required()
    def accountPost():
        form = ForScore(request.form)
        trip_id = request.form.get("trip_id")
        if form.validate_on_submit() is True:
            # Извлекаем объект поездки из базы данных по
            # ее пользователя
            trip = Trip.query.get(trip_id)
            driver = Driver.query.get(trip.driver_id)
            driving_score = form.driving_score.data
            driving_comfort = form.driving_comfort.data
            driving_polite = form.driving_polite.data
            trip.changeScore(driving_score, driving_comfort, driving_polite)
            db.session.commit()
            driver.updateRaiting()
            db.session.commit()
        return redirect(url_for("accountGet"))

    @app.route("/logout", methods=["GET"])
    @jwt_required()
    def logout():
        # Создаем объект ответа, перенаправляющий
        # пользователя на главную страницу
        response = make_response(redirect(url_for("index")))

        # Удаляем cookie с JWT токеном доступа, завершая сеанс пользователя
        response.delete_cookie("access_token_cookie")
        response.delete_cookie("refresh_token_cookie")

        return response

    @app.route("/change_password", methods=["GET"])
    @client_required()
    def changePasswordGet():
        form = ChangePasswordForm()

        # Рендерим шаблон change_password.html и передаем в него форму
        return render_template("changePassword.html", form=form)

    @app.route("/change_password", methods=["POST"])
    @client_required()
    def changePassword():
        form = ChangePasswordForm(request.form)
        if form.validate_on_submit():
            # Получаем идентификатор авторизованного пользователя из JWT токена
            user_id = get_jwt_identity()

            # Извлекаем объект пользователя
            # из базы данных по его идентификатору
            user = User.query.get(user_id)

            # Хешируем старый пароль из формы
            old_password_hash = hashlib.sha256
            (form.old_password.data.encode()).hexdigest()

            if old_password_hash != user.password_hash:
                return jsonify({"message": "Текущий пароль неверный"}), 400

            # Устанавливаем новый пароль для пользователя
            user.changePassword(form.new_password.data)

            # Добавляем измененного пользователя в сессию базы данных
            db.session.add(user)

            # Сохраняем изменения в базе данных
            db.session.commit()

            return jsonify({"message": "Пароль успешно изменен"}), 200

    # Функция обновления access_token
    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refreshToken():
        current_user = get_jwt_identity()
        claims = get_jwt()
        if "client" in claims:
            new_access_token = create_access_token(identity=current_user,
                                                   additional_claims={
                                                       "client": True})
            response = make_response(redirect(url_for("order_get")))
            response.set_cookie("access_token_cookie",
                                value=new_access_token)
        elif "driver" in claims:
            new_access_token = create_access_token(identity=current_user,
                                                   additional_claims={
                                                       "driver": True})
            response = make_response(redirect(url_for("order_get")))
            response.set_cookie("access_token_cookie",
                                value=new_access_token)
        return response

    @app.route("/driver_login", methods=["GET"])
    def driverAuthorizationForm():
        form = LoginForm()
        return render_template("driverLogin.html", form=form)

    @app.route("/driver_login", methods=["POST"])
    def driverAuthorization():
        form = LoginForm(request.form)
        # Валидация
        if form.validate_on_submit() is True:
            try:
                email = form.email.data
                password = form.password.data
                driver = Driver.query.filter_by(email=email).one()
                # Сравниваем хэш введенного пароля с
                # хэшем пароля найденного водителя
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                if password_hash == driver.password_hash:
                    # Создание токена и переход на страницу создания заказа
                    # для уже авторизованного водителя
                    access_token = create_access_token(identity=driver.id,
                                                       additional_claims={
                                                           "driver": True})
                    refresh_token = create_refresh_token(identity=driver.id,
                                                         additional_claims={
                                                             "driver": True})
                    response = make_response(redirect(
                        url_for("getDriverPassage")))
                    response.set_cookie("refresh_token_cookie",
                                        value=refresh_token,
                                        httponly=True, secure=True)
                    response.set_cookie("access_token_cookie",
                                        value=access_token)
                    return response
                else:
                    return jsonify({"message": "Неверный пароль"}), 401
            except NoResultFound:
                return jsonify({"message": "Водитель не найден"}), 404
        # Возвращение подсказок
        return make_response(render_template("driverLogin.html", form=form),
                             400)

    # Форма заказа для водителя
    @app.route("/passage", methods=["GET"])
    @driver_required()
    def getDriverPassage():
        driver_id = get_jwt_identity()
        driver = Driver.query.filter_by(id=driver_id).first()
        # Возвращает форму поиска закаказа,
        # если водитель свободен
        if driver.availability == "Свободен":
            form = PassageForm()
            return render_template("driverPassage.html", form=form)
        else:
            status = "Водитель едет к вам"
            trip_in_process = Trip.query.filter_by(driver_id=driver_id,
                                                   status=status).first()
            # Возваращет форму для перехода на следующий этап поездки,
            # если водитель сейчас находится в пути до клиента
            if trip_in_process is not None:
                form = FlaskForm()
                pickup_location = trip_in_process.pickup_location
                dropoff_location = trip_in_process.dropoff_location
                return render_template("driverAfterTake.html",
                                       pickup_location=pickup_location,
                                       dropoff_location=dropoff_location,
                                       form=form)
            status = "В пути к конечной точке маршрута"
            trip_in_process = Trip.query.filter_by(driver_id=driver_id,
                                                   status=status).first()
            # Возваращет форму для перехода на следующий завершение,
            # если водитель сейчас находится в пути до
            # конечной точки маршрута
            if trip_in_process is not None:
                form = FlaskForm()
                pickup_location = trip_in_process.pickup_location
                dropoff_location = trip_in_process.dropoff_location
                fare = trip_in_process.fare
                return render_template("driverEndTrip.html", form=form,
                                       pickup_location=pickup_location,
                                       dropoff_location=dropoff_location,
                                       fare=fare)

    # Создание заказа для водителя
    @app.route("/passage", methods=["POST"])
    @driver_required()
    def driverPassage():
        form_type = request.form.get("form_type")
        driver_id = get_jwt_identity()
        driver = Driver.query.filter_by(id=driver_id).first()
        # Водитель нажал "Поиск заказа"
        if form_type == "findOrder":
            form = PassageForm(request.form)
            if form.validate_on_submit() is True:
                # Находим первый заказ с текущим статусом "В ожидании"
                status = "В ожидании"
                trip_in_waiting = Trip.query.filter_by(status=status).first()
                if trip_in_waiting is None:
                    return jsonify({"message": "Нет доступных заказов"}), 400
                # Меняем статусы поезкди и водителя
                driver.changeAvailability("В поездке")
                trip_in_waiting.changeStatus("Водитель едет к вам")
                trip_in_waiting.chandeDriverId(driver_id)
                # Получаем местоположение клиента из объекта trip_in_waiting
                pickup_location = trip_in_waiting.pickup_location
                dropoff_location = trip_in_waiting.dropoff_location
                db.session.commit()
                return render_template("driverAfterTake.html",
                                       pickup_location=pickup_location,
                                       dropoff_location=dropoff_location,
                                       form=form)
            return make_response(render_template("driverPassage.html",
                                                 form=form), 400)
        # Водитель подъехал к начальной точке и нажал "Начать поездку"
        elif form_type == "startTrip":
            form = FlaskForm(request.form)
            driver_id = get_jwt_identity()
            status = "Водитель едет к вам"
            trip_in_process = Trip.query.filter_by(driver_id=driver_id,
                                                   status=status).first()
            # Меняем статус поездки
            trip_in_process.changeStatus("В пути к конечной точке маршрута")
            pickup_location = trip_in_process.pickup_location
            dropoff_location = trip_in_process.dropoff_location
            fare = trip_in_process.fare
            db.session.commit()
            return render_template("driverEndTrip.html",
                                   pickup_location=pickup_location,
                                   dropoff_location=dropoff_location,
                                   fare=fare, form=form)
        # Водитель нажал "Завершить поездку"
        elif form_type == "endTrip":
            driver_id = get_jwt_identity()
            status = "В пути к конечной точке маршрута"
            trip_in_process = Trip.query.filter_by(driver_id=driver_id,
                                                   status=status).first()
            fare = trip_in_process.fare
            driver = Driver.query.filter_by(id=driver_id).first()
            driver.changeAvailability("Свободен")
            # Зачисляем деньги в колонку balance водителя
            driver.addMoneyForTrip(fare)
            # Завершаем поездку
            trip_in_process.setCompleted()
            db.session.commit()
            return make_response(redirect(url_for("getDriverPassage")))

    @app.route("/driver_account", methods=["GET"])
    @driver_required()
    def driverAccount():
        # Получаем идентификатор авторизованного водителя из JWT токена
        driver_id = get_jwt_identity()
        # Извлекаем объект пользователя из базы данных по его идентификатору
        driver = Driver.query.get(driver_id)
        # Получаем заказы пользователя из связанной коллекции
        driver_trips = driver.trips
        # Рендерим шаблон driverAccount.html и передаем
        # в него данные пользователя и его заказы
        return render_template("driverAccount.html", driver=driver,
                               trips=driver_trips)