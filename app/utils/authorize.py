import jwt
from flask import jsonify, request
from flask_api import status

from app import app
from functools import wraps

from app.utils.response_generator import ResponseGenerator


def authorize(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        bearer_token = request.headers['Authorization']
        token = str.replace(str(bearer_token), 'Bearer ', '')
        print(token)
        if not token:
            return ResponseGenerator(message='UnAuthorized', status_code=status.HTTP_401_UNAUTHORIZED) \
                .make_error_response()

        try:
            t_data = jwt.decode(token, app.config['SECRET_KEY'])
            returned_value = func(*args, **kwargs)
            return returned_value
        # You can use the JWT errors in exception
        except jwt.InvalidTokenError:
            message = 'Invalid token. Please log in again.'
            return ResponseGenerator(message=message, status_code=status.HTTP_401_UNAUTHORIZED) \
                .make_error_response()
        except Exception as e:
            return ResponseGenerator(message=e.args, status_code=status.HTTP_401_UNAUTHORIZED) \
                .make_error_response()
    return decorated