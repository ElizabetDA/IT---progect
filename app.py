from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Regexp
from wtforms import StringField, PasswordField


app = Flask(__name__)
# Защита от атаки подделки межсайтовых запросов
app.config.from_object("defender")


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


@app.route("/")
def hello_world():
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
        print(name, email, password)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
