from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


# Проверка верификации для клиента
def driver_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["driver"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Доступ запрещен"), 403

        return decorator

    return wrapper


# Проверка верификации для водителя
def client_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["client"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Доступ запрещен"), 403

        return decorator

    return wrapper
