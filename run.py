import connexion
from models import db
from flask_jwt_extended import JWTManager


# Создание экземпляра Flask приложения
app = connexion.FlaskApp(__name__, specification_dir="./")
app.add_api("swagger.yaml")
flask_app = app.app
jwt = JWTManager(flask_app)


# Загрузка конфигурации Flask приложения
flask_app.config.from_pyfile("config.py")

# Привязка SQLAlchemy к flask приложению
db.init_app(flask_app)

if __name__ == "__main__":
    # Создание таблицы User, если она не созадана
    with flask_app.app_context():
        db.create_all()
    app.run()
