from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Regexp
from wtforms import StringField, PasswordField, IntegerField, \
                    validators, SelectField


# Класс формы регистрации
class RegistrationForm(FlaskForm):
    """Форма регистрации нового пользователя."""

    message_empty_field = "Поле не должно быть пустым"
    message_name = "Имя должно содержать только русские буквы"
    message_email = "Неверный почтовый адрес"
    message_password_length = "Пароль должен состоять \
    не менее чем из 8 символов"
    message_no_russian_chars = "Пароль не должен содержать русские буквы"

    username = StringField(
        "Имя:",
        validators=[
            InputRequired(message=message_empty_field),
            Regexp(r"^[А-Яа-яЁё]+$", message=message_name),
        ],
    )
    email = StringField(
        "Электронная почта:",
        validators=[
            InputRequired(message=message_empty_field),
            Email(message=message_email),
        ],
    )
    password = PasswordField(
        "Пароль",
        [
            validators.DataRequired(message=message_empty_field),
            validators.Length(min=8, message=message_password_length),
            validators.Regexp(
                r"^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]+$",
                message=message_no_russian_chars,
            ),
        ],
    )


# Класс формы авторизации
class LoginForm(FlaskForm):
    """Форма авторизации существующего пользователя."""

    message_empty_field = "Поле не должно быть пустым"
    message_email = "Неверный почтовый адрес"
    email = StringField(
        "Введите Email",
        validators=[
            InputRequired(message=message_empty_field),
            Email(message=message_email),
        ],
    )
    password = PasswordField(
        "Введите пароль", validators=[InputRequired
                                      (message=message_empty_field)]
    )


# Класс формы поездки
class TripForm(FlaskForm):
    """Форма создания заказа на поездку."""

    message_adress = "Неверный формат адреса"
    pickup_location = StringField("Место начала поездки")
    dropoff_location = StringField("Место начала поездки")
    payment_method = SelectField(
        "Способ оплаты",
        choices=[("Карта", "Карта"), ("Наличные", "Наличные")],
        validators=[InputRequired()],
    )
    rate = SelectField(
        "Тариф",
        choices=[
            ("Экономный", "Экономный"),
            ("Стандартный", "Стандартный"),
            ("Премиум", "Премиум"),
        ],
    )


# Класс формы смены пароля
class ChangePasswordForm(FlaskForm):
    """Форма смены пароля пользователя."""

    message_empty_field = "Поле не должно быть пустым"
    message_password = "Неверный пароль"
    message_password_length = "Пароль должен состоять \
    не менее чем из 8 символов"
    message_no_russian_chars = "Пароль не должен содержать русские буквы"
    old_password = PasswordField(
        "Введите старый пароль", validators=[InputRequired
                                             (message=message_empty_field)]
    )
    new_password = PasswordField(
        "Пароль",
        [
            validators.DataRequired(message=message_empty_field),
            validators.Length(min=8, message=message_password_length),
            validators.Regexp(
                r"^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]+$",
                message=message_no_russian_chars,
            ),
        ],
    )


# Класс рабочей страницы водителя
class PassageForm(FlaskForm):
    """Форма поиска заказов для водителя.

    Args:
        None

    Returns:
        None
    """

    message_empty_field = "Поле не должно быть пустым"
    message_adress = "Неверный формат адреса"
    location = StringField("Местоположение водителя")


class ChangeUsernameForm(FlaskForm):
    """Форма смены имени пользователя."""

    message_name = "Имя должно содеражать только русские буквы"
    message_empty_field = "Поле не должно быть пустым"
    new_username = StringField(
        "Введите новое имя:",
        validators=[
            InputRequired(message=message_empty_field),
            Regexp(r"^[А-Яа-яЁё]+$", message=message_name),
        ],
    )


class ForScore(FlaskForm):
    """Форма оценки поездки пользователем."""

    driving_score = IntegerField(
        "Стиль вождения", validators=[validators.NumberRange(min=1, max=5)]
    )
    driving_comfort = IntegerField(
        "Комфорт", validators=[validators.NumberRange(min=1, max=5)]
    )
    driving_polite = IntegerField(
        "Вежливость водителя", validators=[validators.NumberRange(min=1,
                                                                  max=5)]
    )
