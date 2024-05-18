from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Regexp, Length
from wtforms import StringField, PasswordField, SelectField


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


class CardForm(FlaskForm):
    date_validate = r"^(0[1-9]|1[0-2])\/([0-9]{2})"
    message_date_validate = 'Неверный формат даты'
    name_validate = r"^[A-Z ]+$"
    message_name_validate = 'Имя должно содержать только заглавные буквы и пробелы'

    card_number = StringField('Номер карты', validators=[InputRequired(), Length(min=16, max=16)])
    card_name = StringField('Имя на карте',
                            validators=[InputRequired(), Regexp(name_validate, message=message_name_validate)])
    expiry_date = StringField('Срок действия',
                              validators=[InputRequired(), Regexp(date_validate, message=message_date_validate)])
    cvv = StringField('CVV', validators=[InputRequired(), Length(min=3, max=3)])
