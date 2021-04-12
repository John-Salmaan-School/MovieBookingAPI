from hashlib import blake2b
import base58
import hmac
import json

# JWT stands for JSON web token. This class is used to create tokens
# and verify tokens based on the hashing algorithm blake2b and hmac as
# well as base58 encoding

# Based on
# https://github.com/hkkio/hikka/blob/master/hikka/tools/jwt.py

class JWT:
    @classmethod
    def create_signed_token(cls, key, data):
        """
        Create a complete JWT token. Exclusively uses blake2b
        HMAC.
        """
        header = json.dumps({"typ": "JWT", "alg": "BLK2B"}).encode("utf-8")
        henc = base58.b58encode_check(header).decode()

        payload = json.dumps(data).encode("utf-8")
        penc = base58.b58encode_check(payload).decode()

        hdata = henc + "." + penc

        d = hmac.new(key, hdata.encode("utf-8"), digestmod=blake2b)
        dig = d.digest()
        denc = base58.b58encode_check(dig).decode()

        token = hdata + "." + denc
        return token

    @classmethod
    def verify_signed_token(cls, key, token):
        """
        Validate token HMAC signature.
        """
        try:
            (header, payload, sig) = token.split(".")
            hdata = header + "." + payload

            d = hmac.new(key, hdata.encode("utf-8"), digestmod=blake2b)
            dig = d.digest()
            denc = base58.b58encode_check(dig).decode()

            return hmac.compare_digest(sig, denc)

        except Exception:
            return False

    @classmethod
    def decode_payload(cls, token):
        """
        Decodes the payload in the token and returns a dict.
        """
        try:
            (header, payload, sig) = token.split(".")
            return json.loads(base58.b58decode_check(payload).decode())

        except Exception:
            return {}

# This function is used to generate a hashed string/key which is
# 32 bits in size.
def hash_key(data, size=32, key=""):
    return blake2b(
        str.encode(data),
        key=str.encode(key),
        digest_size=size
    ).digest()

# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

# Function to check whether the uploaded file is allowed based on extension
def allowed_file(filename: str, ext_list: list):
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ext_list
