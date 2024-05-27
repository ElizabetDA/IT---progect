from flask import render_template, request, jsonify, make_response, \
                redirect, url_for
from models import db, User, Trip, Driver
from forms import (
    RegistrationForm,
    LoginForm,
    TripForm,
    ChangePasswordForm,
    PassageForm,
    ChangeUsernameForm,
    ForScore,
)

from sqlalchemy.orm.exc import NoResultFound
from flask_wtf import FlaskForm
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token,
    get_jwt,
)
from jwtCheck import driver_required, client_required
from api import lenWay
import hashlib


# Функция получения домашней страницы
def register_routes(app):
    """Регистрирует маршруты для приложения Flask.

    Args:
        app (Flask): Объект приложения Flask.

    Returns:
        None
    """

    @app.route("/")
    def index():
        """Обрабатывает запрос на главную страницу.

        Args:

        Returns:
            str: HTML-код главной страницы.
        """

        return render_template("home.html")

    @app.route("/about_us", methods=["GET"])
    def about_us():
        """Обрабатывает запрос на страницу "О нас".

        Args:

        Returns:
            str: HTML-код страницы "О нас".
        """

        return render_template("about_us.html")

    @app.route("/information", methods=["GET"])
    def information():
        """Обрабатывает запрос на страницу "Информация".

        Args:
        Returns:
            str: HTML-код страницы "Информация".
        """

        return render_template("information.html")

    @app.route("/contacts", methods=["GET"])
    def contacts():
        """Обрабатывает запрос на страницу "Контакты".

        Args:


        Returns:
            str: HTML-код страницы "Контакты".
        """

        return render_template("contacts.html")

    @app.route("/qa", methods=["GET"])
    def qa():
        """Обрабатывает запрос на страницу "Часто задаваемые вопросы".

        Args:


        Returns:
            str: HTML-код страницы "Часто задаваемые вопросы".
        """

        return render_template("qa.html")

    @app.route("/pricing", methods=["GET"])
    def pricing():
        """Обрабатывает запрос на страницу "Цены".

        Args:


        Returns:
            str: HTML-код страницы "Цены".
        """

        return render_template("pricing.html")

    # Функция регистрации
    @app.route("/register", methods=["POST"])
    def registration():
        """Обрабатывает запрос на регистрацию нового пользователя.

        Args:

        Returns:
            str: HTML-код страницы с сообщением об успешной регистрации
            или ошибке.
        """

        form = RegistrationForm(request.form)
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data.lower()
            password = form.password.data
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            if User.query.filter_by(email=email).first():
                return render_template(
                    "error.html",
                    message="Пользователь с таким адресом \
                    электронной почты уже существует",
                    previous_url=url_for("registrationForm"),
                )

            new_user = User(username=username, email=email,
                            password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()
            return render_template(
                "success.html",
                message="Пользователь успешно зарегистрирован",
                next_url=url_for("authorizationForm"),
            )

        return make_response(render_template("register.html", form=form), 400)

    # Функция получения формы регистрации
    @app.route("/register", methods=["GET"])
    def registrationForm():
        """Обрабатывает запрос на получение формы регистрации.

        Args:

        Returns:
            str: HTML-код формы регистрации.
        """

        form = RegistrationForm()
        return render_template("register.html", form=form)

    # Функция авторизации
    @app.route("/login", methods=["POST"])
    def authorization():
        """Обрабатывает запрос на авторизацию существующего пользователя.

        Args:
        Returns:
            str: HTML-код страницы с сообщением об успешной авторизации
            или ошибке.
        """

        form = LoginForm(request.form)
        if form.validate_on_submit():
            try:
                email = form.email.data.lower()
                password = form.password.data
                user = User.query.filter_by(email=email).one()
                # Сравниваем хэш введенного пароля с хэшем
                # пароля найденного пользователя

                if user.checkPassword(password):
                    access_token = create_access_token(
                        identity=user.id, additional_claims={"client": True}
                    )
                    refresh_token = create_refresh_token(
                        identity=user.id, additional_claims={"client": True}
                    )
                    response = make_response(redirect(url_for("orderGet")))
                    response.set_cookie(
                        "refresh_token_cookie",
                        value=refresh_token,
                        httponly=True,
                        secure=True,
                    )
                    response.set_cookie("access_token_cookie",
                                        value=access_token)
                    return response
                else:
                    return render_template(
                        "error.html",
                        message="Неверный пароль",
                        previous_url=url_for("authorizationForm"),
                    )
            except NoResultFound:
                return render_template(
                    "error.html",
                    message="Пользователь не найден",
                    previous_url=url_for("authorizationForm"),
                )

        return make_response(render_template("login.html", form=form), 400)

    # Функция получения формы авторизации
    @app.route("/login", methods=["GET"])
    def authorizationForm():
        """Обрабатывает запрос на получение формы авторизации.

        Args:
        Returns:
            str: HTML-код формы авторизации.
        """

        form = LoginForm()
        return render_template("login.html", form=form)

    # Функция получения формы для заказа
    @app.route("/order", methods=["GET"])
    @client_required()
    def orderGet():
        """Обрабатывает запрос на получение формы заказа.

        Args:
        Returns:
            str: HTML-код формы заказа.
        """

        user_id = get_jwt_identity()
        statuses = [
            "В ожидании",
            "Водитель едет к вам",
            "В пути к конечной точке маршрута",
        ]
        trip = Trip.query.filter(
            Trip.status.in_(statuses), Trip.user_id == user_id
        ).first()
        if trip is None:
            form = TripForm()
            return render_template("order.html", form=form)
        else:
            if trip.status == "В ожидании":
                pickup_location = trip.pickup_location
                dropoff_location = trip.dropoff_location
                len_way = trip.len_way
                fare = trip.fare
                status = trip.status
                rate = trip.rate
                return render_template(
                    "trip.html",
                    pickup_location=pickup_location,
                    dropoff_location=dropoff_location,
                    len_way=len_way,
                    fare=fare,
                    status=status,
                    rate=rate,
                )
            else:
                driver_id = trip.driver_id
                driver = Driver.query.filter_by(id=driver_id).first()
                car = driver.car_model
                license_plate = driver.license_plate
                taxist = driver.username
                pickup_location = trip.pickup_location
                dropoff_location = trip.dropoff_location
                len_way = trip.len_way
                fare = trip.fare
                status = trip.status
                rate = trip.rate
                return render_template(
                    "trip.html",
                    pickup_location=pickup_location,
                    dropoff_location=dropoff_location,
                    len_way=len_way,
                    fare=fare,
                    status=status,
                    car=car,
                    license_plate=license_plate,
                    taxist=taxist,
                    rate=rate,
                )

    # Функция создания заказа
    @app.route("/order", methods=["POST"])
    @client_required()
    def orderCreate():
        """Обрабатывает запрос на создание нового заказа.

        Args:
        Returns:
            str: HTML-код страницы с сообщением об успешном создании заказа
            или ошибке.
        """

        form = TripForm(request.form)
        if form.validate_on_submit():
            try:
                pickup_location = form.pickup_location.data
                dropoff_location = form.dropoff_location.data
                rate = form.rate.data
                user_id = get_jwt_identity()
                len_way = lenWay(pickup_location, dropoff_location)
                fare = Trip.calculateFare(len_way, rate)
                payment_method = form.payment_method.data
                new_trip = Trip(
                    pickup_location=pickup_location,
                    dropoff_location=dropoff_location,
                    payment_method=payment_method,
                    user_id=user_id,
                    fare=fare,
                    status="В ожидании",
                    len_way=len_way,
                    rate=rate,
                )
                db.session.add(new_trip)
                db.session.commit()
                return render_template(
                    "success.html",
                    message="Заказ успешно создан",
                    next_url=url_for("orderGet"),
                )
            except Exception:
                return render_template(
                    "error.html",
                    message="Не удалось создать заказ. \
                    Пожалуйста, попробуйте снова.",
                    previous_url=url_for("orderGet"),
                )

    @app.route("/account", methods=["GET"])
    @client_required()
    def accountGet():
        """Обрабатывает запрос на получение страницы аккаунта клиента.

        Args:
        Returns:
            str: HTML-код страницы аккаунта клиента.
        """

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
        """Обрабатывает запрос на отправку оценки поездки.

        Args:
        Returns:
            str: HTML-код страницы с сообщением об успешной отправке оценки
            или ошибке.
        """

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
        """Обрабатывает запрос на выход из аккаунта.

        Args:
        Returns:
            Response: Ответ с перенаправлением на главную страницу
            и удалением cookie с JWT токеном доступа.
        """

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
        """Обрабатывает запрос на получение формы смены пароля.

        Args:
        Returns:
            str: HTML-код формы смены пароля.
        """

        form = ChangePasswordForm()

        # Рендерим шаблон change_password.html и передаем в него форму
        return render_template("changePassword.html", form=form)

    @app.route("/change_password", methods=["POST"])
    @client_required()
    def changePassword():
        """Обрабатывает запрос на смену пароля.

        Args:
        Returns:
            str: HTML-код страницы с сообщением об успешной смене пароля
            или ошибке.
        """

        form = ChangePasswordForm(request.form)
        if form.validate_on_submit():
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user.checkPassword(form.old_password.data):
                return render_template(
                    "error.html",
                    message="Неверный старый пароль",
                    previous_url=url_for("changePasswordGet"),
                )
            if user.checkPassword(form.new_password.data):
                return render_template(
                    "error.html",
                    message="Новый пароль не должен совпадать со старым",
                    previous_url=url_for("changePassword.html"),
                )

            user.changePassword(form.new_password.data)
            db.session.commit()
            return render_template(
                "success.html",
                message="Пароль успешно изменен",
                next_url=url_for("accountGet"),
            )

        return make_response(render_template("changePassword.html",
                                             form=form), 400)

    # Функция обновления access_token
    @app.route("/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refreshToken():
        """Обрабатывает запрос на обновление JWT токена доступа.

        Args:
        Returns:
            Response: Ответ с обновленным JWT токеном доступа.
        """

        current_user = get_jwt_identity()
        claims = get_jwt()
        if "client" in claims:
            new_access_token = create_access_token(
                identity=current_user, additional_claims={"client": True}
            )
            response = make_response(redirect(url_for("order_get")))
            response.set_cookie("access_token_cookie", value=new_access_token)
        elif "driver" in claims:
            new_access_token = create_access_token(
                identity=current_user, additional_claims={"driver": True}
            )
            response = make_response(redirect(url_for("order_get")))
            response.set_cookie("access_token_cookie", value=new_access_token)
        return response

    @app.route("/driver_login", methods=["GET"])
    def driverAuthorizationForm():
        """Обрабатывает запрос на получение формы авторизации водителя.

        Args:
        Returns:
            str: HTML-код формы авторизации водителя.
        """

        form = LoginForm()
        return render_template("driverLogin.html", form=form)

    @app.route("/driver_login", methods=["POST"])
    def driverAuthorization():
        """Обрабатывает запрос на авторизацию водителя.

        Args:
        Returns:
            str: HTML-код страницы с сообщением об успешной авторизации
            водителя или ошибке.
        """

        form = LoginForm(request.form)
        # Валидация
        if form.validate_on_submit() is True:
            try:
                email = form.email.data
                password = form.password.data
                driver = Driver.query.filter_by(email=email).one()
                # Сравниваем хэш введенного пароля с
                # хэшем пароля найденного водителя

                if driver.checkPassword(password):
                    # Создание токена и переход на страницу создания заказа
                    # для уже авторизованного водителя
                    access_token = create_access_token(
                        identity=driver.id, additional_claims={"driver": True}
                    )
                    refresh_token = create_refresh_token(
                        identity=driver.id, additional_claims={"driver": True}
                    )
                    response = make_response(redirect(url_for
                                                      ("getDriverPassage")))
                    response.set_cookie(
                        "refresh_token_cookie",
                        value=refresh_token,
                        httponly=True,
                        secure=True,
                    )
                    response.set_cookie("access_token_cookie",
                                        value=access_token)
                    return response
                else:
                    return jsonify({"message": "Неверный пароль"}), 401
            except NoResultFound:
                return jsonify({"message": "Водитель не найден"}), 404
        # Возвращение подсказок
        return make_response(render_template("driverLogin.html",
                                             form=form), 400)

    # Форма заказа для водителя
    @app.route("/passage", methods=["GET"])
    @driver_required()
    def getDriverPassage():
        """Обрабатывает запрос на получение формы поиска заказов для водителя.

        Args:
        Returns:
            str: HTML-код формы поиска заказов для водителя.
        """

        driver_id = get_jwt_identity()
        driver = Driver.query.filter_by(id=driver_id).first()
        # Возвращает форму поиска закаказа,
        # если водитель свободен
        if driver.availability == "Свободен":
            form = PassageForm()
            return render_template("driverPassage.html", form=form)
        else:
            status = "Водитель едет к вам"
            trip_in_process = Trip.query.filter_by(
                driver_id=driver_id, status=status
            ).first()
            # Возваращет форму для перехода на следующий этап поездки,
            # если водитель сейчас находится в пути до клиента
            if trip_in_process is not None:
                form = FlaskForm()
                pickup_location = trip_in_process.pickup_location
                dropoff_location = trip_in_process.dropoff_location
                return render_template(
                    "driverAfterTake.html",
                    pickup_location=pickup_location,
                    dropoff_location=dropoff_location,
                    form=form,
                )
            status = "В пути к конечной точке маршрута"
            trip_in_process = Trip.query.filter_by(
                driver_id=driver_id, status=status
            ).first()
            # Возваращет форму для перехода на следующий завершение,
            # если водитель сейчас находится в пути до
            # конечной точки маршрута
            if trip_in_process is not None:
                form = FlaskForm()
                pickup_location = trip_in_process.pickup_location
                dropoff_location = trip_in_process.dropoff_location
                fare = trip_in_process.fare
                return render_template(
                    "driverEndTrip.html",
                    form=form,
                    pickup_location=pickup_location,
                    dropoff_location=dropoff_location,
                    fare=fare,
                )

    # Создание заказа для водителя
    @app.route("/passage", methods=["POST"])
    @driver_required()
    def driverPassage():
        """Обрабатывает запрос на создание заказа для водителя.

        Args:
        Returns:
            str: HTML-код страницы с сообщением об успешном создании заказа
            для водителя или ошибке.
        """

        form_type = request.form.get("form_type")
        driver_id = get_jwt_identity()
        driver = Driver.query.filter_by(id=driver_id).first()

        if form_type == "findOrder":
            form = PassageForm(request.form)
            if form.validate_on_submit():
                status = "В ожидании"
                trip_in_waiting = Trip.query.filter_by(
                    status=status, rate=driver.rate
                ).first()
                if trip_in_waiting is None:
                    return render_template(
                        "error.html",
                        message="Нет доступных заказов",
                        previous_url=url_for("getDriverPassage"),
                    )

                driver.changeAvailability("В поездке")
                trip_in_waiting.changeStatus("Водитель едет к вам")
                trip_in_waiting.chandeDriverId(driver_id)
                pickup_location = trip_in_waiting.pickup_location
                dropoff_location = trip_in_waiting.dropoff_location
                db.session.commit()
                return render_template(
                    "driverAfterTake.html",
                    pickup_location=pickup_location,
                    dropoff_location=dropoff_location,
                    form=form,
                )
            return make_response(render_template("driverPassage.html",
                                                 form=form), 400)

        elif form_type == "startTrip":
            form = FlaskForm(request.form)
            status = "Водитель едет к вам"
            trip_in_process = Trip.query.filter_by(
                driver_id=driver_id, status=status
            ).first()
            trip_in_process.changeStatus("В пути к конечной точке маршрута")
            pickup_location = trip_in_process.pickup_location
            dropoff_location = trip_in_process.dropoff_location
            fare = trip_in_process.fare
            db.session.commit()
            return render_template(
                "driverEndTrip.html",
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
                fare=fare,
                form=form,
            )

        elif form_type == "endTrip":
            status = "В пути к конечной точке маршрута"
            trip_in_process = Trip.query.filter_by(
                driver_id=driver_id, status=status
            ).first()
            fare = trip_in_process.fare
            driver.changeAvailability("Свободен")
            driver.addMoneyForTrip(fare)
            trip_in_process.setCompleted()
            db.session.commit()
            return render_template(
                "success.html",
                message="Поездка успешно завершена",
                next_url=url_for("getDriverPassage"),
            )

    @app.route("/driver_account", methods=["GET"])
    @driver_required()
    def driverAccount():
        """Обрабатывает запрос на получение страницы аккаунта водителя.

        Args:
        Returns:
            str: HTML-код страницы аккаунта водителя.
        """

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

    @app.route("/change_username", methods=["POST"])
    @client_required()
    def changeUsername():
        """Обрабатывает запрос на смену имени пользователя.

        Args:
        Returns:
            str: HTML-код страницы с сообщением об успешной смене имени
            или ошибке.
        """

        form = ChangeUsernameForm(request.form)
        if form.validate_on_submit():
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user.username == form.new_username.data:
                return render_template(
                    "error.html",
                    message="Новое имя не должно совпадать со старым",
                    previous_url=url_for("changeUsernameGet"),
                )

            user.username = form.new_username.data
            db.session.commit()
            return render_template(
                "success.html",
                message="Имя успешно изменено",
                next_url=url_for("accountGet"),
            )

        return make_response(render_template("changeUsername.html",
                                             form=form), 400)

    @app.route("/change_username", methods=["GET"])
    @client_required()
    def changeUsernameGet():
        """Обрабатывает запрос на получение формы смены имени пользователя.

        Args:
        Returns:
            str: HTML-код формы смены имени пользователя.
        """

        form = ChangeUsernameForm()
        # Рендерим шаблон change_password.html и передаем в него форму
        return render_template("changeUsername.html", form=form)
