from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Regexp
from wtforms import StringField, PasswordField


# Класс формы регистрации
class RegistrationForm(FlaskForm):
    message_empty_field = "Поле не должно быть пустым"
    message_name = "Имя должно содеражать только русские буквы"
    message_email = "Неверный почтовый адрес"
    username = StringField(
        "Имя:",
        validators=[
            InputRequired(message=message_empty_field),
            Regexp(r"^[А-Яа-яЁё]+$", message=message_name)])
    email = StringField(
        "Электронная почта:",
        validators=[
            InputRequired(message=message_empty_field),
            Email(message=message_email)])
    password = PasswordField(
        "Пароль:", validators=[InputRequired(message=message_empty_field)])


# Класс формы авторизации
class LoginForm(FlaskForm):
    message_empty_field = "Поле не должно быть пустым"
    message_email = "Неверный почтовый адрес"
    email = StringField("Введите Email", validators=[
        InputRequired(message=message_empty_field),
        Email(message=message_email)])
    password = PasswordField("Введите пароль", validators=[
        InputRequired(message=message_empty_field)])


# Класс формы поездки
class TripForm(FlaskForm):
    message_adress = "Неверный формат адреса"
    adress_validate = r"^ул\.\s[A-Za-zА-Яа-я]+\sд\.\s\d{1,3}$"
    pickup_location = StringField("Место начала поездки",
                                  validators=[Regexp(adress_validate,
                                                     message=message_adress)])
    dropoff_location = StringField("Место окончания поездки",
                                   validators=[Regexp(adress_validate,
                                                      message=message_adress)])


# Класс формы смены пароля
class ChangePasswordForm(FlaskForm):
    message_empty_field = "Поле не должно быть пустым"
    message_password = "Неверный пароль"
    old_password = PasswordField("Введите старый пароль", validators=[
        InputRequired(message=message_empty_field)])
    new_password = PasswordField("Введите новый пароль", validators=[
        InputRequired(message=message_empty_field)])


# Класс рабочей страницы водителя
class PassageForm(FlaskForm):
    message_empty_field = "Поле не должно быть пустым"
    message_adress = "Неверный формат адреса"
    adress_validate = r"^ул\.\s[A-Za-zА-Яа-я]+\sд\.\s\d{1,3}$"
    location = StringField("Местоположение водителя",
                           validators=[Regexp(adress_validate,
                                              message=message_adress)])


class ChangeUsernameForm(FlaskForm):
    message_name = "Имя должно содеражать только русские буквы"
    message_empty_field = "Поле не должно быть пустым"
    new_username = StringField(
        "Введите новое имя:",
        validators=[
            InputRequired(message=message_empty_field),
            Regexp(r"^[А-Яа-яЁё]+$", message=message_name)])
