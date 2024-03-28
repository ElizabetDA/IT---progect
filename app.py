from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Regexp
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
# Защита от атаки подделки межсайтовых запросов
app.config.from_object("defender")
import hashlib

# Класс формы регистрации
class RegistrationForm(FlaskForm):
    message_empty_field = "Поле не должно быть пустым"
    message_name = "Имя должно содеражать только русские буквы"
    message_email = "Неверный почтовый адрес"
    name = StringField(
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


class LoginForm(FlaskForm):
    email = StringField("Введите Email", validators=[InputRequired(message="Неверный почтовый адрес"), Email()])
    password = PasswordField('Введите пароль', validators=[InputRequired()])
    submit = SubmitField('Login')


@app.route("/")
def index():
    return "Hello"


# Функция регистрации
@app.route("/register", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    # Проверка валидации(все поля заполнены ли)
    if form.validate_on_submit() is True:
        # Получаем значения из полей name, password, email
        name = form.name.data
        email = form.email.data
        password = form.password.data
        sha256_hash = hashlib.new('sha256')
        sha256_hash.update(password.encode())
        sha256_hex = sha256_hash.hexdigest()
        print(name, email, password, sha256_hex)
    return render_template("index.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
