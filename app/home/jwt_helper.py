from rest_framework_jwt.settings import api_settings
from datetime import datetime
from calendar import timegm


def get_json_web_token(user):

    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = {
        'user_id': user.id,
        'email': user.useremail,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    payload['email'] = user.useremail

    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    return jwt_encode_handler(payload)

def get_token(user):
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload={
        "name":"mugesh",
    }
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    return jwt_encode_handler(payload)