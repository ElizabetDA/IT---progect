from datetime import timedelta
SECRET_KEY = "MAI52"
SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
JWT_SECRET_KEY = "MAI52"
JWT_TOKEN_LOCATION = ["cookies", "headers"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
