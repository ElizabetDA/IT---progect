from flask_sqlalchemy import SQLAlchemy
import connexion


# Создание экземпляра Flask приложения
app = connexion.App(__name__, specification_dir="./")
app.add_api("swagger.yaml")
flask_app = app.app

# Загрузка конфигурации Flask приложения
flask_app.config.from_pyfile("config.py")

# Создание экземпляра SQLAlchemy и привязка к Flask приложению
db = SQLAlchemy(flask_app)


# Создание базы данных, если еще не  была создана
with flask_app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
