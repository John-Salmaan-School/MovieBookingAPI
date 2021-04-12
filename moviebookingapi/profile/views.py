from flask import request, Blueprint
from ..token import authenticate

blueprint = Blueprint("profile", __name__, url_prefix="/profile/")

@blueprint.route("/info", methods=["GET"])
def info():
    result = {"data": {}, "error": None}
    user = authenticate(request)

    if user[0]:
        result["data"] = {
            "name": user[1].name
        }
        return result
    else:
        result["error"] = user[1]
        return result
