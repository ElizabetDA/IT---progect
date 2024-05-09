from datetime import timedelta

SECRET_KEY = "MAI52"
SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
JWT_SECRET_KEY = "MAI52"
JWT_TOKEN_LOCATION = "cookies"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
JWT_COOKIE_CSRF_PROTECT = False
API_KEY = "261dd9c7-7968-4e32-924a-14a15afb00c7"
