from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Regexp
from wtforms import StringField, PasswordField, IntegerField, validators, SelectField


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
    pickup_location = StringField("Место начала поездки")
    dropoff_location = StringField("Место начала поездки")
    payment_method = SelectField('Способ оплаты', choices=[('Карта', 'Карта'), ('Наличные', 'Наличные')],
                                 validators=[InputRequired()])

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
    location = StringField("Местоположение водителя")
    
    
class ForScore(FlaskForm):
    driving_score = IntegerField(
        "Стиль вождения",
        validators=[validators.NumberRange(min=1, max=5)])
    driving_comfort = IntegerField(
        "Комфорт",
        validators=[validators.NumberRange(min=1, max=5)])
    driving_polite = IntegerField(
        "Вежливость водителя",
        validators=[validators.NumberRange(min=1, max=5)])
