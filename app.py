from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField, PasswordField


app = Flask(__name__)
# Защита от атаки подделки межсайтовых запросов
app.config.from_object("defender")


# Класс формы регистрации
class RegistrationForm(FlaskForm):
    name = StringField("Имя:", validators=[InputRequired()])
    password = PasswordField("Пароль:", validators=[InputRequired()])


@app.route("/")
def hello_world():
    return "Hello"


# Функция регистрации
@app.route("/register", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    # Проверка валидации(все поля заполнены ли)
    if form.validate_on_submit() is True:
        # Получаем значения из полей name и password
        name = form.name.data
        password = form.password.data
        print(name, password)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
