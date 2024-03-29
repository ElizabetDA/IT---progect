from flask import render_template, redirect, url_for
import hashlib
from forms import RegistrationForm, LoginForm


def register_routes(app):
    @app.route("/")
    def homePage():
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

    # Функция авторизации
    @app.route("/login", methods=["GET", "POST"])
    def login():
        form = LoginForm()
        if form.validate_on_submit() is True:
            return redirect(url_for("homePage"))
        return render_template("login.html", form=form)
