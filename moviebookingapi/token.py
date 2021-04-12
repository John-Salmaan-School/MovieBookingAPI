# Holds the Token class that is used to create and validate authentication tokens
from datetime import timedelta, datetime
from .services import UserService
from .utils import JWT, hash_key
from flask import request
from pony import orm
import config

jwt = JWT()

# Based on
# https://github.com/hkkio/hikka/blob/master/hikka/auth.py#L13

class Token(object):

    @classmethod
    # Creates a JWT used for authentication that expires
    # after 2 days
    def create(cls, action, data, expire=None, secret=None):
        time_diff = expire if expire else timedelta(minutes=5)
        token_exp = int(datetime.timestamp(datetime.utcnow() + time_diff))
        token_key = secret if secret else config.secret

        return jwt.create_signed_token(hash_key(data=token_key), {
            "action": action,
            "expire": token_exp,
            "meta": data
        })

    @classmethod
    # Method used to verify the token to see if it has expired or not
    def verify(cls, token, secret=None):
        key = secret if secret else config.secret
        valid = jwt.verify_signed_token(hash_key(key), token)
        payload = jwt.decode_payload(token)

        # If there is no expiry date set in the JWT, then it is not valid
        if "expire" not in payload:
            valid = False
        # If the token expiry is less than the current timestamp, then it
        # is no longer valid
        elif payload["expire"] < int(datetime.timestamp(datetime.utcnow())):
            valid = False

        return valid

    @classmethod
    # Method to simplify decoding a payload in other files without needing
    # to import jwt
    def payload(cls, token):
        return jwt.decode_payload(token)

# This function is used to authenticate the token passed in the header
# POST request. The function will be used for the /profile route

# Based on
# https://github.com/hkkio/hikka/blob/master/hikka/decorators.py

@orm.db_session
def authenticate(r: request):
    token = r.headers.get("Authentication")

    valid = Token.verify(token=token)
    payload = Token.payload(token=token)

    if valid and payload["action"] == "login":
        user = UserService.get_by_email(email=payload["meta"])

        if not user:
            return [False, "User does not exist"]

        return [True, user]

    return [False, "Token is invalid"]
