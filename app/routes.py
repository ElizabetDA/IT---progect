from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import RegistrationForm, LoginForm
from app.models import User
from sqlalchemy.orm.exc import NoResultFound
import hashlib


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
        password_hash = hashlib.sha256(form.password.data.encode()).hexdigest()
        # Проверяем существует ли пользователь в нашей БД, если уже существует, то не добавляем в БД
        if User.query.filter_by(email=email).first():
            ...
        else:
            new_user = User(name=name, email=email, password_hash=password_hash)
            # Добавляем пользователя в БД
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("index"))

    return render_template("index.html", form=form)


# Функция авторизации
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit() is True:
        email = form.email.data
        password_hash = hashlib.sha256(form.password.data.encode()).hexdigest()
        try:
            # Находим пользователя в БД по email. Метод one() выдаст исключение Noresultfound в случае,
            # если результатов нет
            user = User.query.filter_by(email=email).one()
            # Сравниваем хэш введенного пароля с  хэшем пароля найденного пользователя
            if password_hash == user.password_hash:
                return redirect(url_for("index"))
            else:
                ...
        except NoResultFound:
            ...

    return render_template("login.html", form=form)
