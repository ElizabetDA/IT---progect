from models import db
from flask_jwt_extended import JWTManager
from flask import Flask
from lokir import register_routes
from flask_wtf.csrf import CSRFProtect
import os
import hashlib


# Создание экземпляра Flask приложения
app = Flask(__name__)
app.static_folder = os.path.join(app.root_path, 'static')
jwt = JWTManager(app)

# Загрузка конфигурации Flask приложения
app.config.from_pyfile("config.py")
csrf = CSRFProtect(app)
# Привязка SQLAlchemy к flask приложению
db.init_app(app)
register_routes(app)
print(hashlib.sha256("123".encode()).hexdigest())
if __name__ == "__main__":
    # Создание таблицы User, если она не созадана
    with app.app_context():
        db.create_all()
    app.run(debug=True)
